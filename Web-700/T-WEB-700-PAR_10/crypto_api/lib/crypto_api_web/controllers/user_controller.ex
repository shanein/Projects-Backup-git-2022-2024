defmodule CryptoApiWeb.UserController do
  use CryptoApiWeb, :controller

  alias CryptoApi.Accounts
  alias CryptoApi.Accounts.User

  action_fallback CryptoApiWeb.FallbackController

  #Only admin
  def index(conn, %{"admin" => admin_id}) do
    if Accounts.is_admin(admin_id) do
      users = Accounts.list_users()
      render(conn, "index.json", users: users)
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("not_admin.json")
    end
  end

  #Any user
  def login(conn, %{"email" => email, "password" => password}) do
    user = Accounts.get_user_by_email!(email)
    if user != nil and Accounts.checkCredentials!(user, password) do
      render(conn, "show.json", user: user)
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Any user
  def show(conn, %{"user_id" => id}) do
    user = Accounts.get_user!(id)
    if user != nil do
      render(conn, "show.json", user: user)
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Any user
  def create(conn, %{"user" => user_params}) do
    if user_params["password"] != nil do
      user_params = Map.put(user_params, "password", Bcrypt.Base.hash_password(user_params["password"], Bcrypt.Base.gen_salt(12, true)))
      user_params = Map.put(user_params, "role", "user")
      with {:ok, %User{} = user} <- Accounts.create_user(user_params) do
        conn
        |> put_status(:created)
        |> put_resp_header("location", Routes.user_path(conn, :show, user))
        |> render("show.json", user: user)
      end
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Admin only
  def update(conn, %{"admin" => admin_id, "user_id" => user_id,"user" => user_params}) do
    if Accounts.is_admin(admin_id) do
      user_params = Map.delete(user_params, "password")
      user = Accounts.get_user!(user_id)
      if user != nil do
        with {:ok, %User{} = user} <- Accounts.update_user(user, user_params) do
          render(conn, "show.json", user: user)
        end
      else
          conn
          |> put_view(CryptoApiWeb.ErrorView)
          |> render("bad_arguments.json")
      end
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("not_admin.json")
    end
  end

  #Any user
  def update(conn, %{"user_id" => id, "user" => user_params}) do
    user = Accounts.get_user!(id)
    user_params = Map.drop(user_params, ["password", "role"])
    if user != nil do
      with {:ok, %User{} = user} <- Accounts.update_user(user, user_params) do
        render(conn, "show.json", user: user)
      end
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Any user
  def update_pw(conn, %{"user_id" => id, "user" => user_params}) do
    user = Accounts.get_user!(id)
    if user != nil and Accounts.checkCredentials!(user, user_params["old_password"]) do
      user_params = %{"password" => Bcrypt.Base.hash_password(user_params["password"], Bcrypt.Base.gen_salt(12, true))}
      with {:ok, %User{} = user} <- Accounts.update_user(user, user_params) do
        render(conn, "show.json", user: user)
      end
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Any user
  def delete(conn, %{"user_id" => id}) do
    user = Accounts.get_user!(id)
    if user != nil do
      with {:ok, %User{}} <- Accounts.delete_user(user) do
        send_resp(conn, :no_content, "")
      end
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end
end
