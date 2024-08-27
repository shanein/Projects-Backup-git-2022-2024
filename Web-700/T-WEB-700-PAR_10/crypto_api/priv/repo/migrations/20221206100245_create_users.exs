defmodule CryptoApi.Repo.Migrations.CreateUsers do
  use Ecto.Migration

  def change do
    create table(:users, primary_key: false) do
      add :id, :binary_id, primary_key: true
      add :email, :string, null: false
      add :password, :string, null: false
      add :firstname, :string
      add :lastname, :string
      add :role, :string, default: "user"
      add :profile_picture, :binary

      timestamps()
    end
    create unique_index(:users, :email, name: :emails_index)
  end
end
