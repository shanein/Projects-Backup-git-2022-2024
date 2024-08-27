defmodule CryptoApi.Ressources do
  @moduledoc """
  The Ressources context.
  """

  import Ecto.Query, warn: false
  alias CryptoApi.Repo

  alias CryptoApi.Ressources.Article

  @doc """
  Returns the list of articles.

  ## Examples

      iex> list_articles()
      [%Article{}, ...]

  """
  def list_articles(preloads) do
    from(
      a in Article
    )
    |> Repo.all
    |> Repo.preload(preloads)
  end

  def get_article_by_crypto!(crypto_id, preloads) do
    from(
      a in Article,
      where: a.crypto_id == ^crypto_id
    )
    |> Repo.all
    |> Repo.preload(preloads)
  end

  @doc """
  Gets a single article.

  Raises `Ecto.NoResultsError` if the Article does not exist.

  ## Examples

      iex> get_article!(123)
      %Article{}

      iex> get_article!(456)
      ** (Ecto.NoResultsError)

  """
  def get_article!(id, preloads) do
    from(
      a in Article,
      where: a.id == ^id
    )
    |> Repo.one
    |> Repo.preload(preloads)
  end

  @doc """
  Creates a article.

  ## Examples

      iex> create_article(%{field: value})
      {:ok, %Article{}}

      iex> create_article(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_article(attrs \\ %{}, crypto) do
    %Article{crypto: crypto}
    |> Article.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a article.

  ## Examples

      iex> update_article(article, %{field: new_value})
      {:ok, %Article{}}

      iex> update_article(article, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_article(%Article{} = article, attrs) do
    article
    |> Article.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a article.

  ## Examples

      iex> delete_article(article)
      {:ok, %Article{}}

      iex> delete_article(article)
      {:error, %Ecto.Changeset{}}

  """
  def delete_article(%Article{} = article) do
    Repo.delete(article)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking article changes.

  ## Examples

      iex> change_article(article)
      %Ecto.Changeset{data: %Article{}}

  """
  def change_article(%Article{} = article, attrs \\ %{}) do
    Article.changeset(article, attrs)
  end
end
