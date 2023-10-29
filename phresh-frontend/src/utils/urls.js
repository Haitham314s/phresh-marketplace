import { BE_URL } from "../constants"

/**
 * Formats API request URLs
 *
 * @param {String} base - url string representing api endpoint without query params
 * @param {Object} params - query params to format and append to end of url
 */
export const formatURLWithQueryParams = (base, params) => {
  if (!params || Object.keys(params)?.length === 0) return base

  const query = Object.entries(params)
    .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
    .join("&")

  return `${base}?${query}`
}

/**
 * Formats API request URLs
 *
 * @param {String} url - url string representing relative path to api endpoint
 * @param {Object} params - query params to format at end of url
 */
export const formatURL = (url, params) => {
  const fullURL = `${BE_URL}${url}`

  return formatURLWithQueryParams(fullURL, params)
}
