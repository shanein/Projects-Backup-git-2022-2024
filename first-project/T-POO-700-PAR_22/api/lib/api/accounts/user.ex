defmodule Api.Accounts.User do
  use Ecto.Schema
  import Ecto.Changeset

  schema "users" do
    field :email, :string
    field :username, :string
    field :role, :string
    field :password, :string
    has_many :workingtime, Api.Time.Workingtime
    has_many :clock, Api.Time.Clock

    timestamps()
  end

  @doc false
  def changeset(user, attrs) do
    user
    |> cast(attrs, [:username, :email, :role, :password])
    |> validate_required([:username, :email, :password])
    |> validate_format(:email, ~r/^\w([\.]?\w+)*@\w+([\.-]?\w+)*(\.\w+)$/u,
         message: "This must match email format"
       )
    |> validate_format(:role, ~r/admin|user|manager/u,
         message: "Role must be a defined role"
       )
  end
end
