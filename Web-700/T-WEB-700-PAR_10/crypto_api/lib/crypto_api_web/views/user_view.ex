defmodule CryptoApiWeb.UserView do
  use CryptoApiWeb, :view
  alias CryptoApiWeb.UserView

  def render("index.json", %{users: users}) do
    %{data: render_many(users, UserView, "user.json")}
  end

  def render("show.json", %{user: user}) do
    %{data: render_one(user, UserView, "user.json")}
  end

  def render("user.json", %{user: user}) do
    %{
      id: user.id,
      email: user.email,
      firstname: user.firstname,
      lastname: user.lastname,
      role: user.role,
      profile_picture: user.profile_picture
    }
  end
end
