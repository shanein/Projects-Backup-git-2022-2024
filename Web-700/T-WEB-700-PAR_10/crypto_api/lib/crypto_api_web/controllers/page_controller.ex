defmodule CryptoApiWeb.PageController do
  use CryptoApiWeb, :controller

  def index(conn, _params) do
    render(conn, "index.html")
  end
end
