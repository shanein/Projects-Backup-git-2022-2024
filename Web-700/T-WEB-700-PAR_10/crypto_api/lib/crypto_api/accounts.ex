defmodule CryptoApi.Accounts do
  @moduledoc """
  The Accounts context.
  """

  import Ecto.Query, warn: false
  alias CryptoApi.Repo

  alias CryptoApi.Accounts
  alias CryptoApi.Accounts.User

  def is_admin(user_id) do
      user = Accounts.get_user!(user_id)
      user != nil and user.role == "admin"
  end

  @doc """
  Returns the list of users.

  ## Examples

      iex> list_users()
      [%User{}, ...]

  """
  def list_users do
    from(
      u in User
    )
    |> Repo.all
  end

  @doc """
  Gets a single user.

  Raises `Ecto.NoResultsError` if the User does not exist.

  ## Examples

      iex> get_user!(123)
      %User{}

      iex> get_user!(456)
      ** (Ecto.NoResultsError)

  """
  def get_user!(id) do
    try do
      from(
        u in User,
        where: u.id == ^id
      )
      |> Repo.one
    rescue
      Ecto.Query.CastError ->
        from(
          u in User,
          where: u.email == ^id
        )
        |> Repo.one
    end
  end

  def get_user_by_email!(email) do
    from(
      u in User,
      where: u.email == ^email
    )
    |> Repo.one
  end

  def checkCredentials!(user, password) do
    Bcrypt.verify_pass(password, user.password)
  end

  @doc """
  Creates a user.

  ## Examples

      iex> create_user(%{field: value})
      {:ok, %User{}}

      iex> create_user(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_user(attrs \\ %{}) do
    %User{}
    |> User.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a user.

  ## Examples

      iex> update_user(user, %{field: new_value})
      {:ok, %User{}}

      iex> update_user(user, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_user(%User{} = user, attrs) do
    user
    |> User.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a user.

  ## Examples

      iex> delete_user(user)
      {:ok, %User{}}

      iex> delete_user(user)
      {:error, %Ecto.Changeset{}}

  """
  def delete_user(%User{} = user) do
    Repo.delete(user)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking user changes.

  ## Examples

      iex> change_user(user)
      %Ecto.Changeset{data: %User{}}

  """
  def change_user(%User{} = user, attrs \\ %{}) do
    User.changeset(user, attrs)
  end

  alias CryptoApi.Accounts.UserCrypto

  @doc """
  Returns the list of users_cryptos.

  ## Examples

      iex> list_users_cryptos()
      [%UserCrypto{}, ...]

  """
  def list_users_cryptos(preloads) do
    from(
      uc in UserCrypto
    )
    |> Repo.all
    |> Repo.preload(preloads)
  end

  def get_user_crypto_from_user!(user_id, preloads) do
    from(
      uc in UserCrypto,
      where: uc.user_id == ^user_id
    )
    |> Repo.all
    |> Repo.preload(preloads)
  end

  @doc """
  Gets a single user_crypto.

  Raises `Ecto.NoResultsError` if the User crypto does not exist.

  ## Examples

      iex> get_user_crypto!(123)
      %UserCrypto{}

      iex> get_user_crypto!(456)
      ** (Ecto.NoResultsError)

  """
  def get_user_crypto!(id, preloads) do
    from(
      uc in UserCrypto,
      where: uc.id == ^id
    )
    |> Repo.one
    |> Repo.preload(preloads)
  end

  def get_user_crypto_from_data!(crypto_id, user_id) do
    from(
      uc in UserCrypto,
      where: uc.user_id == ^user_id
      and uc.crypto_id == ^crypto_id
    )
    |> Repo.one
  end

  @doc """
  Creates a user_crypto.

  ## Examples

      iex> create_user_crypto(%{field: value})
      {:ok, %UserCrypto{}}

      iex> create_user_crypto(%{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def create_user_crypto(attrs \\ %{}, crypto) do
    %UserCrypto{crypto: crypto}
    |> UserCrypto.changeset(attrs)
    |> Repo.insert()
  end

  @doc """
  Updates a user_crypto.

  ## Examples

      iex> update_user_crypto(user_crypto, %{field: new_value})
      {:ok, %UserCrypto{}}

      iex> update_user_crypto(user_crypto, %{field: bad_value})
      {:error, %Ecto.Changeset{}}

  """
  def update_user_crypto(%UserCrypto{} = user_crypto, attrs) do
    user_crypto
    |> UserCrypto.changeset(attrs)
    |> Repo.update()
  end

  @doc """
  Deletes a user_crypto.

  ## Examples

      iex> delete_user_crypto(user_crypto)
      {:ok, %UserCrypto{}}

      iex> delete_user_crypto(user_crypto)
      {:error, %Ecto.Changeset{}}

  """
  def delete_user_crypto(%UserCrypto{} = user_crypto) do
    Repo.delete(user_crypto)
  end

  @doc """
  Returns an `%Ecto.Changeset{}` for tracking user_crypto changes.

  ## Examples

      iex> change_user_crypto(user_crypto)
      %Ecto.Changeset{data: %UserCrypto{}}

  """
  def change_user_crypto(%UserCrypto{} = user_crypto, attrs \\ %{}) do
    UserCrypto.changeset(user_crypto, attrs)
  end
end
