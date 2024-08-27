defmodule ApiWeb.UserController do
  use ApiWeb, :controller

  alias Api.Accounts
  alias Api.Accounts.User

  action_fallback ApiWeb.FallbackController

  def login(conn, %{"user" => user_params}) do
    users = Accounts.checkCredentials!(user_params["identifier"],user_params["password"])
    if users == [nil] or users == [] do
      raise Ecto.NoResultsError, message: "Identifier or password is wrong"
    end
    render(conn, "index.json", users: users)
  end

  def showAttr(conn, attr) do
    users = Accounts.get_user_by_attr!(attr["email"],attr["username"])
    if users == [] do
      raise Ecto.NoResultsError, message: "No entry found with given fields"
    end
    render(conn, "index.json", users: users)
  end

  def show(conn, %{"id" => id}) do
    user = Accounts.get_user!(id)
    render(conn, "show.json", user: user)
  end

  def create(conn, %{"user" => user_params}) do
    user_params = Map.put(user_params, "password", Bcrypt.Base.hash_password(user_params["password"], Bcrypt.Base.gen_salt(12, true)))
    with {:ok, %User{} = user} <- Accounts.create_user(user_params) do
      conn
      |> put_status(:created)
      |> put_resp_header("location", Routes.user_path(conn, :show, user))
      |> render("show.json", user: user)
    end
  end

  def update(conn, %{"id" => id, "user" => user_params}) do
    user_params = if user_params["password"] != nil do
      Map.put(user_params, "password", Bcrypt.Base.hash_password(user_params["password"], Bcrypt.Base.gen_salt(12, true)))
    else
      user_params
    end
    user = Accounts.get_user!(id)

    with {:ok, %User{} = user} <- Accounts.update_user(user, user_params) do
      render(conn, "show.json", user: user)
    end
  end

  def delete(conn, %{"id" => id}) do
    user = Accounts.get_user!(id)

    with {:ok, %User{}} <- Accounts.delete_user(user) do
      send_resp(conn, :no_content, "")
    end
  end
end
