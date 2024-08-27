defmodule CryptoApi.RessourcesFixtures do
  @moduledoc """
  This module defines test helpers for creating
  entities via the `CryptoApi.Ressources` context.
  """

  @doc """
  Generate a article.
  """
  def article_fixture(attrs \\ %{}) do
    {:ok, article} =
      attrs
      |> Enum.into(%{
        src: "some src"
      })
      |> CryptoApi.Ressources.create_article()

    article
  end
end
