defmodule CryptoApi.Repo.Migrations.CreateArticles do
  use Ecto.Migration

  def change do
    create table(:articles, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :src, :string, null: false
      add :crypto_id, references(:cryptos, type: :binary_id, on_delete: :delete_all), null: false

      timestamps()
    end
    create unique_index(:articles, :src, name: :articles_index)
  end
end
