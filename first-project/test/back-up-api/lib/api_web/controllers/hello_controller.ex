defmodule ApiWeb.HelloController do
  use ApiWeb, :controller

  def world(conn, %{"name" => name}) do
    render(conn, "world.html", name: name)
  end
end
