import React from "react"
import { BrowserRouter, Route, Routes } from "react-router-dom"
import {
  LandingPage,
  Layout,
  LoginPage,
  NotFoundPage,
  ProfilePage,
  RegistrationPage
} from "../../components"

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/registration" element={<RegistrationPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}
