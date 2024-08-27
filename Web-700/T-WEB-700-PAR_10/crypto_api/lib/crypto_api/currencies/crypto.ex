defmodule CryptoApi.Currencies.Crypto do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :binary_id, autogenerate: true}

  schema "cryptos" do
    field :name, :string

    timestamps()
  end

  @doc false
  def changeset(crypto, attrs) do
    crypto
    |> cast(attrs, [:name])
    |> validate_required([:name])
    |> unique_constraint(:unique_cryptos, name: :cryptos_index)
  end
end
