defmodule CryptoApiWeb.ArticleController do
  use CryptoApiWeb, :controller

  alias CryptoApi.Ressources
  alias CryptoApi.Ressources.Article

  alias CryptoApi.Accounts

  action_fallback CryptoApiWeb.FallbackController


  #Any user
  def index(conn, _params) do
    preloads = [:crypto]
    articles = Ressources.list_articles(preloads)
    render(conn, "index.json", articles: articles)
  end

  #Any user
  def index_by_crypto(conn, %{"crypto_name" => crypto_name}) do
    preloads = [:crypto]
    crypto = CryptoApi.Currencies.get_crypto_by_name!(crypto_name)
    articles = if crypto != nil do
      Ressources.get_article_by_crypto!(crypto.id, preloads)
    end
    if articles != nil do
      render(conn, "index.json", articles: articles)
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Any user
  def show(conn, %{"id" => id}) do
    preloads = [:crypto]
    article = Ressources.get_article!(id, preloads)
    if article != nil do
      render(conn, "show.json", article: article)
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Admin only
  def create(conn, %{"admin" => admin_id, "article" => article_params, "crypto" => crypto_name}) do
    if Accounts.is_admin(admin_id) do
      crypto = CryptoApi.Currencies.get_crypto_by_name!(crypto_name)
      article_params = if crypto != nil do
         Map.put(article_params, "crypto_id", crypto.id)
      end
      if article_params != nil do
        with {:ok, %Article{} = article} <- Ressources.create_article(article_params, crypto) do
          conn
          |> put_status(:created)
          |> put_resp_header("location", Routes.article_path(conn, :show, article))
          |> render("show.json", article: article)
        end
      else
        conn
        |> put_view(CryptoApiWeb.ErrorView)
        |> render("bad_arguments.json")
      end
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("not_admin.json")
    end
  end

  #Admin only
  def update(conn, %{"admin" => admin_id, "id" => id, "article" => article_params, "crypto" => crypto_name}) do
    preloads = [:crypto]
    if Accounts.is_admin(admin_id) do
      article = Ressources.get_article!(id, preloads)
      {article_params, crypto} = if crypto_name != nil do
        c = CryptoApi.Currencies.get_crypto_by_name!(crypto_name)
        {Map.put(article_params, "crypto_id", c.id), c}
      else
        c = if article != nil do
          CryptoApi.Currencies.get_crypto!(article.crypto_id)
        end
        {article_params, c}
      end
      if crypto != nil do
        article = Map.put(article, :crypto_id, crypto.id)
        article = Map.put(article, :crypto, crypto)
        with {:ok, %Article{} = article} <- Ressources.update_article(article, article_params) do
          render(conn, "show.json", article: article)
        end
      else
        conn
        |> put_view(CryptoApiWeb.ErrorView)
        |> render("bad_arguments.json")
      end
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("not_admin.json")
    end
  end

  #Admin only
  def delete(conn, %{"admin" => admin_id, "id" => id}) do
    if Accounts.is_admin(admin_id) do
      article = Ressources.get_article!(id, [])
      if article != nil do
        with {:ok, %Article{}} <- Ressources.delete_article(article) do
          send_resp(conn, :no_content, "")
        end
      else
        conn
        |> put_view(CryptoApiWeb.ErrorView)
        |> render("bad_arguments.json")
      end
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("not_admin.json")
    end
  end
end
