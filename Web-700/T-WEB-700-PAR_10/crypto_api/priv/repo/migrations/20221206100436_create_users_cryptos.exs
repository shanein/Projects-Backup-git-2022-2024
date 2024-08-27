defmodule CryptoApi.Repo.Migrations.CreateUsersCryptos do
  use Ecto.Migration

  def change do
    create table(:users_cryptos, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :user_id, references(:users, type: :binary_id, on_delete: :delete_all), primary_key: true
      add :crypto_id, references(:cryptos, type: :binary_id, on_delete: :delete_all), primary_key: true
      timestamps()
    end
    create index(:users_cryptos, [:user_id])
    create index(:users_cryptos, [:crypto_id])
    create unique_index(:users_cryptos, [:user_id, :crypto_id], name: :subs_index)
  end
end
