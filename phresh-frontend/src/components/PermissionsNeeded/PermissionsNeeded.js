import { EuiEmptyPrompt } from "@elastic/eui"
import React from "react"

export default function PermissionsNeeded({ element, isAllowed = false }) {
  if (!isAllowed) {
    return (
      <EuiEmptyPrompt
        iconType="securityApp"
        iconColor={null}
        title={<h2>Access Denied</h2>}
        body={<p>You are not authorized to access this content.</p>}
      />
    )
  }

  return element
}
