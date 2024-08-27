defmodule CryptoApiWeb.UserCryptoController do
  use CryptoApiWeb, :controller

  alias CryptoApi.Accounts
  alias CryptoApi.Accounts.UserCrypto

  action_fallback CryptoApiWeb.FallbackController

  #Admin only
  def index(conn, %{"admin" => admin_id}) do
    preloads = [:crypto]
    if Accounts.is_admin(admin_id) do
      users_cryptos = Accounts.list_users_cryptos(preloads)
      render(conn, "index.json", users_cryptos: users_cryptos)
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("not_admin.json")
    end
  end

  #Any user
  def index_by_user(conn, %{"user_id" => user_id}) do
    preloads = [:crypto]
    user_cryptos = Accounts.get_user_crypto_from_user!(user_id, preloads)
    render(conn, "index.json", users_cryptos: user_cryptos)
  end

  #Any user
  def show(conn, %{"id" => id}) do
    preloads = [:crypto]
    user_crypto = Accounts.get_user_crypto!(id, preloads)
    if user_crypto != nil do
      render(conn, "show.json", user_crypto: user_crypto)
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Any user
  def create(conn, %{"crypto_name" => crypto_name, "id" => id}) do
    crypto = CryptoApi.Currencies.get_crypto_by_name!(crypto_name)
    user = Accounts.get_user!(id)
    user_crypto_params = if user != nil and crypto != nil do
      %{"user_id" => user.id, "crypto_id" => crypto.id}
    end
    if user_crypto_params != nil do
      with {:ok, %UserCrypto{} = user_crypto} <- Accounts.create_user_crypto(user_crypto_params, crypto) do
        conn
        |> put_status(:created)
        |> put_resp_header("location", Routes.user_crypto_path(conn, :show, user_crypto))
        |> render("show-basic.json", user_crypto: user_crypto)
      end
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Any user
  def delete(conn, %{"crypto_name" => crypto_name, "id" => id}) do
    crypto = CryptoApi.Currencies.get_crypto_by_name!(crypto_name)
    user = Accounts.get_user!(id)
    user_crypto = if user != nil and crypto != nil do
      Accounts.get_user_crypto_from_data!(crypto.id, user.id)
    end
    if user_crypto != nil do
      with {:ok, %UserCrypto{}} <- Accounts.delete_user_crypto(user_crypto) do
        send_resp(conn, :no_content, "")
      end
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end
end
