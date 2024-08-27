defmodule CryptoApiWeb.CryptoController do
  use CryptoApiWeb, :controller

  alias CryptoApi.Currencies
  alias CryptoApi.Currencies.Crypto

  alias CryptoApi.Accounts

  action_fallback CryptoApiWeb.FallbackController

  #Any user
  def index(conn, _params) do
    cryptos = Currencies.list_cryptos()
    render(conn, "index.json", cryptos: cryptos)
  end

  #Any user
  def show(conn, %{"id" => crypto_name}) do
    crypto = Currencies.get_crypto_by_name!(crypto_name)
    if crypto != nil do
      render(conn, "show.json", crypto: crypto)
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Any user
  def show_crypto_detail(conn, %{"crypto_name" => crypto_name}) do
    crypto = Currencies.get_crypto_by_name!(crypto_name)
    if crypto != nil do
      render(conn, "show_detail.json", crypto: crypto)
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Any user
  def show_crypto_variations(conn, %{"crypto_name" => crypto_name, "length" => length}) do
    crypto = Currencies.get_crypto_by_name!(crypto_name)
    if crypto != nil do
      render(conn, "show_variation.json", crypto: crypto, length: length)
    else
      conn
      |> put_view(CryptoApiWeb.ErrorView)
      |> render("bad_arguments.json")
    end
  end

  #Admin only
  def create(conn, %{"admin" => admin_id, "crypto" => crypto_params}) do
    if Accounts.is_admin(admin_id) do
      if crypto_params["name"] != nil do
        crypto_params = Map.put(crypto_params, "name", String.downcase(crypto_params["name"]))
        url = "https://api.coingecko.com/api/v3/coins/" <> crypto_params["name"]
        case HTTPoison.get(url) do
          {:ok, %{status_code: 200}} ->
            with {:ok, %Crypto{} = crypto} <- Currencies.create_crypto(crypto_params) do
              conn
              |> put_status(:created)
              |> put_resp_header("location", Routes.crypto_path(conn, :show, crypto))
              |> render("show.json", crypto: crypto)
            end
          {:ok, %{status_code: 404}} ->
            conn
            |> put_view(CryptoApiWeb.ErrorView)
            |> render("bad_arguments.json")
          {:error, _details} ->
            conn
            |> put_view(CryptoApiWeb.ErrorView)
            |> render("not_found.json")
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

  #Admin only
  def delete(conn, %{"admin" => admin_id, "id" => crypto_name}) do
    if Accounts.is_admin(admin_id) do
      crypto = Currencies.get_crypto_by_name!(crypto_name)
      if crypto != nil do
        with {:ok, %Crypto{}} <- Currencies.delete_crypto(crypto) do
          send_resp(conn, :no_content, "")
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
end
