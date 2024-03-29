import axios from "axios"
import { BE_URL } from "../constants"
import apiClient from "../services/apiClient"
import { Actions as cleaningActions } from "./cleanings"
import initialState from "./initialState"

export const REQUEST_LOGIN = "@@auth/REQUEST_LOGIN"
export const REQUEST_LOGIN_FAILURE = "@@auth/REQUEST_LOGIN_FAILURE"
export const REQUEST_LOGIN_SUCCESS = "@@auth/REQUEST_LOGIN_SUCCESS"
export const REQUEST_LOG_USER_OUT = "@@auth/REQUEST_LOG_USER_OUT"

export const REQUEST_USER_SIGN_UP = "@@auth/REQUEST_USER_SIGN_UP"
export const REQUEST_USER_SIGN_UP_SUCCESS = "@@auth/REQUEST_USER_SIGN_UP_SUCCESS"
export const REQUEST_USER_SIGN_UP_FAILURE = "@@auth/REQUEST_USER_SIGN_UP_FAILURE"

export const FETCHING_USER_FROM_TOKEN = "@@auth/FETCHING_USER_FROM_TOKEN"
export const FETCHING_USER_FROM_TOKEN_SUCCESS = "@@auth/FETCHING_USER_FROM_TOKEN_SUCCESS"
export const FETCHING_USER_FROM_TOKEN_FAILURE = "@@auth/FETCHING_USER_FROM_TOKEN_FAILURE"

export default function authReducer(state = initialState.auth, action = {}) {
  switch (action.type) {
    case REQUEST_LOGIN:
      return {
        ...state,
        isLoading: true
      }
    case REQUEST_LOGIN_FAILURE:
      return {
        ...state,
        isLoading: false,
        error: action.error,
        user: {}
      }
    case REQUEST_LOGIN_SUCCESS:
      return {
        ...state,
        isLoading: false,
        error: null
      }
    case REQUEST_USER_SIGN_UP:
      return {
        ...state,
        isLoading: true
      }
    case REQUEST_USER_SIGN_UP_SUCCESS:
      return {
        ...state,
        isLoading: false,
        error: null
      }
    case REQUEST_USER_SIGN_UP_FAILURE:
      return {
        ...state,
        isLoading: false,
        isAuthenticated: false,
        error: action.error
      }
    case FETCHING_USER_FROM_TOKEN:
      return {
        ...state,
        isLoading: true
      }
    case FETCHING_USER_FROM_TOKEN_SUCCESS:
      return {
        ...state,
        isAuthenticated: true,
        userLoaded: true,
        isLoading: false,
        user: action.data
      }
    case FETCHING_USER_FROM_TOKEN_FAILURE:
      return {
        ...state,
        isAuthenticated: false,
        userLoaded: true,
        isLoading: false,
        error: action.error,
        user: {}
      }
    case REQUEST_LOG_USER_OUT:
      return {
        ...initialState.auth
      }
    default:
      return state
  }
}

export const Actions = {}

Actions.requestUserLogin = ({ email, password }) => {
  return async (dispatch) => {
    dispatch({ type: REQUEST_LOGIN })

    // create the url-encoded form data
    const formData = new FormData()
    formData.set("username", email)
    formData.set("password", password)

    // set the request headers
    const headers = {
      "Content-Type": "application/x-www-form-urlencoded"
    }

    try {
      // make the actual HTTP request to our API
      const res = await axios({
        method: `POST`,
        url: `${BE_URL}/auth/token`,
        data: formData,
        headers
      })
      console.log(res)

      // stash the access_token our server returns
      const access_token = res?.data?.access_token
      localStorage.setItem("access_token", access_token)

      // dispatch the fetch user from token action creator
      return dispatch(Actions.fetchUserFromToken(access_token))
    } catch (error) {
      console.log(error)

      // dispatch the failure action
      return dispatch({ type: REQUEST_LOGIN_FAILURE, error: error?.message })
    }
  }
}

Actions.registerNewUser = ({ username, email, password }) => {
  return (dispatch) =>
    dispatch(
      apiClient({
        url: `/auth/user`,
        method: `POST`,
        types: {
          REQUEST: REQUEST_USER_SIGN_UP,
          SUCCESS: REQUEST_USER_SIGN_UP_SUCCESS,
          FAILURE: REQUEST_USER_SIGN_UP_FAILURE
        },
        options: {
          data: { username, email, password },
          params: {}
        },
        onSuccess: (res) => {
          // stash the access_token our server returns
          const access_token = res?.data?.access_token?.access_token
          localStorage.setItem("access_token", access_token)

          return dispatch(Actions.fetchUserFromToken(access_token))
        },
        onFailure: (res) => ({ success: false, status: res.status, error: res.error })
      })
    )
}

Actions.fetchUserFromToken = () => {
  return (dispatch) => {
    return dispatch(
      apiClient({
        url: `/auth/user`,
        method: `GET`,
        types: {
          REQUEST: FETCHING_USER_FROM_TOKEN,
          SUCCESS: FETCHING_USER_FROM_TOKEN_SUCCESS,
          FAILURE: FETCHING_USER_FROM_TOKEN_FAILURE
        },
        options: {
          data: {},
          params: {}
        },
        onSuccess: (res) => {
          dispatch(cleaningActions.fetchAllUserOwnedCleaningJobs())
          return { success: true, status: res.status, data: res.data }
        }
      })
    )
  }
}

// Actions.fetchUserFromToken = (access_token) => {
//   return async (dispatch) => {
//     dispatch({ type: FETCHING_USER_FROM_TOKEN })

//     const token = access_token ? access_token : localStorage.getItem("access_token")

//     const headers = {
//       "Content-Type": "application/json",
//       Authorization: `Bearer ${token}`
//     }

//     try {
//       const res = await axios({
//         method: `GET`,
//         url: `http://localhost:8000/api/users/me/`,
//         headers
//       })
//       console.log(res)

//       return dispatch({ type: FETCHING_USER_FROM_TOKEN_SUCCESS, data: res.data })
//     } catch (error) {
//       console.log(error)

//       return dispatch({ type: FETCHING_USER_FROM_TOKEN_FAILURE, error: error.message })
//     }
//   }
// }

Actions.logUserOut = () => {
  localStorage.removeItem("access_token")

  return {
    type: REQUEST_LOG_USER_OUT
  }
}
