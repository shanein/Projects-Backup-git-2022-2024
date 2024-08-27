defmodule CryptoApiWeb.CryptoControllerTest do
  use CryptoApiWeb.ConnCase

  import CryptoApi.CurrenciesFixtures

  alias CryptoApi.Currencies.Crypto

  @create_attrs %{
    name: "some name"
  }
  @update_attrs %{
    name: "some updated name"
  }
  @invalid_attrs %{name: nil}

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  describe "index" do
    test "lists all cryptos", %{conn: conn} do
      conn = get(conn, Routes.crypto_path(conn, :index))
      assert json_response(conn, 200)["data"] == []
    end
  end

  describe "create crypto" do
    test "renders crypto when data is valid", %{conn: conn} do
      conn = post(conn, Routes.crypto_path(conn, :create), crypto: @create_attrs)
      assert %{"id" => id} = json_response(conn, 201)["data"]

      conn = get(conn, Routes.crypto_path(conn, :show, id))

      assert %{
               "id" => ^id,
               "name" => "some name"
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, Routes.crypto_path(conn, :create), crypto: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "update crypto" do
    setup [:create_crypto]

    test "renders crypto when data is valid", %{conn: conn, crypto: %Crypto{id: id} = crypto} do
      conn = put(conn, Routes.crypto_path(conn, :update, crypto), crypto: @update_attrs)
      assert %{"id" => ^id} = json_response(conn, 200)["data"]

      conn = get(conn, Routes.crypto_path(conn, :show, id))

      assert %{
               "id" => ^id,
               "name" => "some updated name"
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn, crypto: crypto} do
      conn = put(conn, Routes.crypto_path(conn, :update, crypto), crypto: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "delete crypto" do
    setup [:create_crypto]

    test "deletes chosen crypto", %{conn: conn, crypto: crypto} do
      conn = delete(conn, Routes.crypto_path(conn, :delete, crypto))
      assert response(conn, 204)

      assert_error_sent 404, fn ->
        get(conn, Routes.crypto_path(conn, :show, crypto))
      end
    end
  end

  defp create_crypto(_) do
    crypto = crypto_fixture()
    %{crypto: crypto}
  end
end
