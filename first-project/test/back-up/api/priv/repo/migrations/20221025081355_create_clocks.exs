defmodule Api.Repo.Migrations.CreateClocks do
  use Ecto.Migration

  def change do
    create table(:clocks) do
      add :time, :naive_datetime, null: false
      add :status, :boolean, default: true, null: false
      add :user, references(:users, on_delete: :nothing), null: false

      timestamps()
    end

    create index(:clocks, [:user])
  end
end
