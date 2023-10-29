import React from "react"
import { Route, Routes } from "react-router-dom"
import { CleaningJobsHome, CleaningJobView, NotFoundPage } from "../../components"

export default function CleaningJobsPage() {
  return (
    <>
      <Routes>
        <Route path="/" element={<CleaningJobsHome />} />
        <Route path=":cleaning_id" element={<CleaningJobView />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </>
  )
}
