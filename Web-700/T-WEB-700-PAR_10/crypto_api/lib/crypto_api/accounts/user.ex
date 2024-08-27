defmodule CryptoApi.Accounts.User do
  use Ecto.Schema
  import Ecto.Changeset

  @primary_key {:id, :binary_id, autogenerate: true}
  
  schema "users" do
    field :email, :string
    field :firstname, :string
    field :lastname, :string
    field :password, :string
    field :role, :string
    field :profile_picture, :binary

    timestamps()
  end

  @doc false
  def changeset(user, attrs) do
    user
    |> cast(attrs, [:email, :firstname, :lastname, :password, :role, :profile_picture])
    |> validate_required([:email, :password, :role])
    |> validate_format(:email, ~r/^\w([\.]?\w+)*@\w+([\.-]?\w+)*(\.\w+)$/u,
         message: "This must match email format"
    )
    |> validate_format(:role, ~r/admin|user/u,
         message: "Role must be a defined role"
    )
    |> unique_constraint(:unique_users, name: :emails_index)
  end
end
