defmodule CryptoApi.CurrenciesTest do
  use CryptoApi.DataCase

  alias CryptoApi.Currencies

  describe "cryptos" do
    alias CryptoApi.Currencies.Crypto

    import CryptoApi.CurrenciesFixtures

    @invalid_attrs %{name: nil}

    test "list_cryptos/0 returns all cryptos" do
      crypto = crypto_fixture()
      assert Currencies.list_cryptos() == [crypto]
    end

    test "get_crypto!/1 returns the crypto with given id" do
      crypto = crypto_fixture()
      assert Currencies.get_crypto!(crypto.id) == crypto
    end

    test "create_crypto/1 with valid data creates a crypto" do
      valid_attrs = %{name: "some name"}

      assert {:ok, %Crypto{} = crypto} = Currencies.create_crypto(valid_attrs)
      assert crypto.name == "some name"
    end

    test "create_crypto/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Currencies.create_crypto(@invalid_attrs)
    end

    test "update_crypto/2 with valid data updates the crypto" do
      crypto = crypto_fixture()
      update_attrs = %{name: "some updated name"}

      assert {:ok, %Crypto{} = crypto} = Currencies.update_crypto(crypto, update_attrs)
      assert crypto.name == "some updated name"
    end

    test "update_crypto/2 with invalid data returns error changeset" do
      crypto = crypto_fixture()
      assert {:error, %Ecto.Changeset{}} = Currencies.update_crypto(crypto, @invalid_attrs)
      assert crypto == Currencies.get_crypto!(crypto.id)
    end

    test "delete_crypto/1 deletes the crypto" do
      crypto = crypto_fixture()
      assert {:ok, %Crypto{}} = Currencies.delete_crypto(crypto)
      assert_raise Ecto.NoResultsError, fn -> Currencies.get_crypto!(crypto.id) end
    end

    test "change_crypto/1 returns a crypto changeset" do
      crypto = crypto_fixture()
      assert %Ecto.Changeset{} = Currencies.change_crypto(crypto)
    end
  end
end
