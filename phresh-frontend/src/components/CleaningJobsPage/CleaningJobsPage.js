import { CleaningJobView, CleaningJobsHome, NotFoundPage } from "components";
import React from "react";
import { Route, Routes } from "react-router-dom";

export default function CleaningJobsPage() {
  return (
    <>
      <Routes>
        <Route path="/" element={<CleaningJobsHome />} />
        <Route path=":cleaningId/*" element={<CleaningJobView />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </>
  );
}
