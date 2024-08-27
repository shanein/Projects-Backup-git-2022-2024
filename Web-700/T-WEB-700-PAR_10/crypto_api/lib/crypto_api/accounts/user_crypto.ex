defmodule CryptoApi.Accounts.UserCrypto do
  use Ecto.Schema
  import Ecto.Changeset

  alias CryptoApi.Currencies
  alias CryptoApi.Accounts

  @primary_key {:id, :binary_id, autogenerate: true}
  @foreign_key_type :binary_id

  schema "users_cryptos" do
    belongs_to :user, Accounts.User
    belongs_to :crypto, Currencies.Crypto

    timestamps()
  end

  @doc false
  def changeset(user_crypto, attrs) do
    user_crypto
    |> cast(attrs, [:user_id, :crypto_id])
    |> validate_required([:user_id, :crypto_id])
    |> unique_constraint(:unique_subs, name: :subs_index)
  end
end
