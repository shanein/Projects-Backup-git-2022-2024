defmodule CryptoApi.RessourcesTest do
  use CryptoApi.DataCase

  alias CryptoApi.Ressources

  describe "articles" do
    alias CryptoApi.Ressources.Article

    import CryptoApi.RessourcesFixtures

    @invalid_attrs %{src: nil}

    test "list_articles/0 returns all articles" do
      article = article_fixture()
      assert Ressources.list_articles() == [article]
    end

    test "get_article!/1 returns the article with given id" do
      article = article_fixture()
      assert Ressources.get_article!(article.id) == article
    end

    test "create_article/1 with valid data creates a article" do
      valid_attrs = %{src: "some src"}

      assert {:ok, %Article{} = article} = Ressources.create_article(valid_attrs)
      assert article.src == "some src"
    end

    test "create_article/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Ressources.create_article(@invalid_attrs)
    end

    test "update_article/2 with valid data updates the article" do
      article = article_fixture()
      update_attrs = %{src: "some updated src"}

      assert {:ok, %Article{} = article} = Ressources.update_article(article, update_attrs)
      assert article.src == "some updated src"
    end

    test "update_article/2 with invalid data returns error changeset" do
      article = article_fixture()
      assert {:error, %Ecto.Changeset{}} = Ressources.update_article(article, @invalid_attrs)
      assert article == Ressources.get_article!(article.id)
    end

    test "delete_article/1 deletes the article" do
      article = article_fixture()
      assert {:ok, %Article{}} = Ressources.delete_article(article)
      assert_raise Ecto.NoResultsError, fn -> Ressources.get_article!(article.id) end
    end

    test "change_article/1 returns a article changeset" do
      article = article_fixture()
      assert %Ecto.Changeset{} = Ressources.change_article(article)
    end
  end
end
