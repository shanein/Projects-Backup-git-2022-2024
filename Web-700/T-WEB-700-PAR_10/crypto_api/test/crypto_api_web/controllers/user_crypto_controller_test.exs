defmodule CryptoApiWeb.UserCryptoControllerTest do
  use CryptoApiWeb.ConnCase

  import CryptoApi.AccountsFixtures

  alias CryptoApi.Accounts.UserCrypto

  @create_attrs %{

  }
  @update_attrs %{

  }
  @invalid_attrs %{}

  setup %{conn: conn} do
    {:ok, conn: put_req_header(conn, "accept", "application/json")}
  end

  describe "index" do
    test "lists all users_cryptos", %{conn: conn} do
      conn = get(conn, Routes.user_crypto_path(conn, :index))
      assert json_response(conn, 200)["data"] == []
    end
  end

  describe "create user_crypto" do
    test "renders user_crypto when data is valid", %{conn: conn} do
      conn = post(conn, Routes.user_crypto_path(conn, :create), user_crypto: @create_attrs)
      assert %{"id" => id} = json_response(conn, 201)["data"]

      conn = get(conn, Routes.user_crypto_path(conn, :show, id))

      assert %{
               "id" => ^id
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn} do
      conn = post(conn, Routes.user_crypto_path(conn, :create), user_crypto: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "update user_crypto" do
    setup [:create_user_crypto]

    test "renders user_crypto when data is valid", %{conn: conn, user_crypto: %UserCrypto{id: id} = user_crypto} do
      conn = put(conn, Routes.user_crypto_path(conn, :update, user_crypto), user_crypto: @update_attrs)
      assert %{"id" => ^id} = json_response(conn, 200)["data"]

      conn = get(conn, Routes.user_crypto_path(conn, :show, id))

      assert %{
               "id" => ^id
             } = json_response(conn, 200)["data"]
    end

    test "renders errors when data is invalid", %{conn: conn, user_crypto: user_crypto} do
      conn = put(conn, Routes.user_crypto_path(conn, :update, user_crypto), user_crypto: @invalid_attrs)
      assert json_response(conn, 422)["errors"] != %{}
    end
  end

  describe "delete user_crypto" do
    setup [:create_user_crypto]

    test "deletes chosen user_crypto", %{conn: conn, user_crypto: user_crypto} do
      conn = delete(conn, Routes.user_crypto_path(conn, :delete, user_crypto))
      assert response(conn, 204)

      assert_error_sent 404, fn ->
        get(conn, Routes.user_crypto_path(conn, :show, user_crypto))
      end
    end
  end

  defp create_user_crypto(_) do
    user_crypto = user_crypto_fixture()
    %{user_crypto: user_crypto}
  end
end
