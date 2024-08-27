defmodule CryptoApi.Ressources.Article do
  use Ecto.Schema
  import Ecto.Changeset

  alias CryptoApi.Currencies

  @primary_key {:id, :binary_id, autogenerate: true}
  @foreign_key_type :binary_id

  schema "articles" do
    field :src, :string

    belongs_to :crypto, Currencies.Crypto
    timestamps()
  end

  @doc false
  def changeset(article, attrs) do
    article
    |> cast(attrs, [:src, :crypto_id])
    |> validate_required([:src, :crypto_id])
    |> unique_constraint(:unique_articles, name: :articles_index)
  end
end
