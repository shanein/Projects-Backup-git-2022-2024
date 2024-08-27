defmodule CryptoApi.Repo.Migrations.CreateCryptos do
  use Ecto.Migration

  def change do
    create table(:cryptos, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :name, :string, null: false

      timestamps()
    end
    create unique_index(:cryptos, :name, name: :cryptos_index)
  end
end
