defmodule CryptoApi.AccountsTest do
  use CryptoApi.DataCase

  alias CryptoApi.Accounts

  describe "users" do
    alias CryptoApi.Accounts.User

    import CryptoApi.AccountsFixtures

    @invalid_attrs %{email: nil, firstname: nil, lastname: nil, password: nil, role: nil}

    test "list_users/0 returns all users" do
      user = user_fixture()
      assert Accounts.list_users() == [user]
    end

    test "get_user!/1 returns the user with given id" do
      user = user_fixture()
      assert Accounts.get_user!(user.id) == user
    end

    test "create_user/1 with valid data creates a user" do
      valid_attrs = %{email: "some email", firstname: "some firstname", lastname: "some lastname", password: "some password", role: "some role"}

      assert {:ok, %User{} = user} = Accounts.create_user(valid_attrs)
      assert user.email == "some email"
      assert user.firstname == "some firstname"
      assert user.lastname == "some lastname"
      assert user.password == "some password"
      assert user.role == "some role"
    end

    test "create_user/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Accounts.create_user(@invalid_attrs)
    end

    test "update_user/2 with valid data updates the user" do
      user = user_fixture()
      update_attrs = %{email: "some updated email", firstname: "some updated firstname", lastname: "some updated lastname", password: "some updated password", role: "some updated role"}

      assert {:ok, %User{} = user} = Accounts.update_user(user, update_attrs)
      assert user.email == "some updated email"
      assert user.firstname == "some updated firstname"
      assert user.lastname == "some updated lastname"
      assert user.password == "some updated password"
      assert user.role == "some updated role"
    end

    test "update_user/2 with invalid data returns error changeset" do
      user = user_fixture()
      assert {:error, %Ecto.Changeset{}} = Accounts.update_user(user, @invalid_attrs)
      assert user == Accounts.get_user!(user.id)
    end

    test "delete_user/1 deletes the user" do
      user = user_fixture()
      assert {:ok, %User{}} = Accounts.delete_user(user)
      assert_raise Ecto.NoResultsError, fn -> Accounts.get_user!(user.id) end
    end

    test "change_user/1 returns a user changeset" do
      user = user_fixture()
      assert %Ecto.Changeset{} = Accounts.change_user(user)
    end
  end

  describe "users_cryptos" do
    alias CryptoApi.Accounts.UserCrypto

    import CryptoApi.AccountsFixtures

    @invalid_attrs %{}

    test "list_users_cryptos/0 returns all users_cryptos" do
      user_crypto = user_crypto_fixture()
      assert Accounts.list_users_cryptos() == [user_crypto]
    end

    test "get_user_crypto!/1 returns the user_crypto with given id" do
      user_crypto = user_crypto_fixture()
      assert Accounts.get_user_crypto!(user_crypto.id) == user_crypto
    end

    test "create_user_crypto/1 with valid data creates a user_crypto" do
      valid_attrs = %{}

      assert {:ok, %UserCrypto{} = user_crypto} = Accounts.create_user_crypto(valid_attrs)
    end

    test "create_user_crypto/1 with invalid data returns error changeset" do
      assert {:error, %Ecto.Changeset{}} = Accounts.create_user_crypto(@invalid_attrs)
    end

    test "update_user_crypto/2 with valid data updates the user_crypto" do
      user_crypto = user_crypto_fixture()
      update_attrs = %{}

      assert {:ok, %UserCrypto{} = user_crypto} = Accounts.update_user_crypto(user_crypto, update_attrs)
    end

    test "update_user_crypto/2 with invalid data returns error changeset" do
      user_crypto = user_crypto_fixture()
      assert {:error, %Ecto.Changeset{}} = Accounts.update_user_crypto(user_crypto, @invalid_attrs)
      assert user_crypto == Accounts.get_user_crypto!(user_crypto.id)
    end

    test "delete_user_crypto/1 deletes the user_crypto" do
      user_crypto = user_crypto_fixture()
      assert {:ok, %UserCrypto{}} = Accounts.delete_user_crypto(user_crypto)
      assert_raise Ecto.NoResultsError, fn -> Accounts.get_user_crypto!(user_crypto.id) end
    end

    test "change_user_crypto/1 returns a user_crypto changeset" do
      user_crypto = user_crypto_fixture()
      assert %Ecto.Changeset{} = Accounts.change_user_crypto(user_crypto)
    end
  end
end
