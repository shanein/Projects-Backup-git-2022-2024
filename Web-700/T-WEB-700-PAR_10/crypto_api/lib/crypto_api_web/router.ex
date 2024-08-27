defmodule CryptoApiWeb.Router do
  use CryptoApiWeb, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_live_flash
    plug :put_root_layout, {CryptoApiWeb.LayoutView, :root}
    plug :put_secure_browser_headers
  end

  pipeline :api do
    plug :accepts, ["json"]
  end

  scope "/", CryptoApiWeb do
    pipe_through :browser

    #Anonymous functions
    get "/login", UserController, :login
    post "/register", UserController, :create

    #Sub functions
    post "/:crypto_name/subscribe", UserCryptoController, :create
    delete "/:crypto_name/unsubscribe", UserCryptoController, :delete
    get "/:user_id/subscriptions", UserCryptoController, :index_by_user

    #User functions
    get "/:user_id/profile", UserController, :show
    delete "/:user_id/profile", UserController, :delete
    put "/:user_id/profile", UserController, :update
    put "/:user_id/password", UserController, :update_pw

    #Resources
    resources "/users", UserController, except: [:new, :edit, :update, :create, :delete, :show]
    resources "/cryptos", CryptoController, except: [:new, :edit, :update]
    resources "/articles", ArticleController, except: [:new, :edit]
    resources "/subscribers", UserCryptoController, except: [:new, :edit, :update, :create, :delete, :index]

    get "/", PageController, :index
  end

  # Other scopes may use custom stacks.
  # scope "/api", CryptoApiWeb do
  #   pipe_through :api
  # end

  scope "/cryptos", CryptoApiWeb do
    pipe_through :browser

    get "/detail/:crypto_name", CryptoController, :show_crypto_detail
    get "/variation/:crypto_name", CryptoController, :show_crypto_variations

    get "/:crypto_name/articles", ArticleController, :index_by_crypto
  end

  # Enables LiveDashboard only for development
  #
  # If you want to use the LiveDashboard in production, you should put
  # it behind authentication and allow only admins to access it.
  # If your application does not have an admins-only section yet,
  # you can use Plug.BasicAuth to set up some basic authentication
  # as long as you are also using SSL (which you should anyway).
  if Mix.env() in [:dev, :test] do
    import Phoenix.LiveDashboard.Router

    scope "/" do
      pipe_through :browser

      live_dashboard "/dashboard", metrics: CryptoApiWeb.Telemetry
    end
  end

  # Enables the Swoosh mailbox preview in development.
  #
  # Note that preview only shows emails that were sent by the same
  # node running the Phoenix server.
  if Mix.env() == :dev do
    scope "/dev" do
      pipe_through :browser

      forward "/mailbox", Plug.Swoosh.MailboxPreview
    end
  end
end
