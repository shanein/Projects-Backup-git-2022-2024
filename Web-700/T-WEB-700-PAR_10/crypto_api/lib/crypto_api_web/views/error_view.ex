defmodule CryptoApiWeb.ErrorView do
  use CryptoApiWeb, :view
  alias CryptoApiWeb.ErrorView

  # If you want to customize a particular status code
  # for a certain format, you may uncomment below.
  # def render("500.html", _assigns) do
  #   "Internal Server Error"
  # end

  def render("not_admin.json", _assigns) do
    error = %{code: 401, message: "You are not an admin"}
    %{errors: [render_one(error, ErrorView, "error.json")]}
  end

  def render("not_found.json", _assigns) do
    error = %{code: 404, message: "Resource not found"}
    %{errors: [render_one(error, ErrorView, "error.json")]}
  end

  def render("bad_arguments.json", _assigns) do
    error = %{code: 400, message: "Bad arguments given"}
    %{errors: [render_one(error, ErrorView, "error.json")]}
  end

  def render("error.json", %{error: error}) do
    %{
      code: error.code,
      message: error.message
    }
  end

  # By default, Phoenix returns the status message from
  # the template name. For example, "404.html" becomes
  # "Not Found".
  def template_not_found(template, _assigns) do
    Phoenix.Controller.status_message_from_template(template)
  end
end
