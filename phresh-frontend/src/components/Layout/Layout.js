import "@elastic/eui/dist/eui_theme_light.css"
import euiVars from "@elastic/eui/dist/eui_theme_light.json"
import React from "react"
import { Helmet } from "react-helmet"
import styled, { ThemeProvider } from "styled-components"
import "../../assets/css/fonts.css"
import "../../assets/css/override.css"
import { Navbar } from "../../components"

const customTheme = {
  ...euiVars,
  euiTitleColor: "dodgerblue"
}

const StyledLayout = styled.div`
  width: 100%;
  max-width: 100vw;
  min-height: 100vh;
  background: rgb(224, 228, 234);
  display: flex;
  flex-direction: column;
`

const StyledMain = styled.main`
  min-height: calc(100vh - ${(props) => props.theme.euiHeaderHeight} - 1px);
  display: flex;
  flex-direction: column;
`

export default function Layout({ children }) {
  return (
    <React.Fragment>
      <Helmet>
        <meta charSet="utf-8" />
        <title>Phresh Cleaners</title>
        <link rel="canonical" href="https://phreshcleaners.com" />
      </Helmet>
      <ThemeProvider theme={customTheme}>
        <StyledLayout>
          <Navbar />
          <StyledMain>{children}</StyledMain>
        </StyledLayout>
      </ThemeProvider>
    </React.Fragment>
  )
}