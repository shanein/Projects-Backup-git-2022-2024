defmodule ApiWeb.ClockController do
  use ApiWeb, :controller

  alias Api.Time
  alias Api.Time.Clock

  action_fallback ApiWeb.FallbackController

  def showAll(conn, %{"user" => userID}) do
    clocks = Time.get_user_clock!(userID)
    if clocks == [] do
      raise Ecto.NoResultsError, message: "No entry found with given fields"
    end
    render(conn, "index.json", clocks: clocks)
  end

  def create(conn, %{"user" => userID, "clock" => clock_params}) do
    #Check if user id given in body and in the url does match
    if clock_params["user_id"] != nil do
      if clock_params["user_id"] != userID do
        raise ArgumentError, message: "The 'user_id' given in request does not match 'user_id' in URL."
      end
    end

    #Force user_id from URL by default
    clock_params = Map.put(clock_params, "user_id", userID)

    #Format time for the status check
    formatedTime = NaiveDateTime.from_iso8601!(clock_params["time"])

    #Gets all working time from the user to check the status
    workingtimes = Time.get_all_workingtimes!(userID, nil, nil)

    #Count the number of times where clock is in a working time (Not very optimized)
    matches = Enum.sum(for workingtime <- workingtimes do
      if NaiveDateTime.compare(workingtime.start, formatedTime) != "gt" and NaiveDateTime.compare(workingtime.end, formatedTime) != "lt" do
        1
      else
        0
      end
    end)

    #Set status to true if there's any match, else false
    clock_params = if matches > 0 do
      Map.put(clock_params, "status", true)
    else
      Map.put(clock_params, "status", false)
    end

    with {:ok, %Clock{} = clock} <- Time.create_clock(clock_params) do
      conn
      |> put_status(:created)
      |> put_resp_header("location", Routes.clock_path(conn, :showAll, clock))
      |> render("show.json", clock: clock)
    end
  end
end
