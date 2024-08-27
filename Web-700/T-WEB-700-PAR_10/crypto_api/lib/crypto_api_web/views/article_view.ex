defmodule CryptoApiWeb.ArticleView do
  use CryptoApiWeb, :view
  alias CryptoApiWeb.ArticleView

  alias CryptoApiWeb.Utils
  alias CryptoApiWeb.CryptoView

  def render("index.json", %{articles: articles}) do
    articles = Utils.replaceCryptos(articles)
    %{data: render_many(articles, ArticleView, "article.json")}
  end

  def render("show.json", %{article: article}) do
    article = Map.put(article, :crypto, CryptoView.getCryptoInfo([article.crypto]))
    %{data: render_one(article, ArticleView, "article.json")}
  end

  def render("article.json", %{article: article}) do
    %{
      id: article.id,
      src: article.src,
      crypto: article.crypto
    }
  end
end
