import {
  EuiAvatar,
  EuiHorizontalRule,
  EuiIcon,
  EuiPage,
  EuiPageBody,
  EuiPageContent,
  EuiPageContentBody,
  EuiPageHeader,
  EuiPageHeaderSection,
  EuiText,
  EuiTitle
} from "@elastic/eui"
import moment from "moment"
import React from "react"
import { connect } from "react-redux"
import styled from "styled-components"

const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`
const StyledEuiPageHeader = styled(EuiPageHeader)`
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 2rem;

  & h1 {
    font-size: 3.5rem;
  }
`
const StyledEuiPageContentBody = styled(EuiPageContentBody)`
  display: flex;
  flex-direction: column;
  align-items: center;

  & h2 {
    margin-bottom: 1rem;
  }
`

function ProfilePage({ user }) {
  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <StyledEuiPageHeader>
          <EuiPageHeaderSection>
            <EuiTitle size="l">
              <h1>Profile</h1>
            </EuiTitle>
          </EuiPageHeaderSection>
        </StyledEuiPageHeader>
        <EuiPageContent verticalPosition="center" horizontalPosition="center">
          <StyledEuiPageContentBody>
            <EuiAvatar
              size="xl"
              name={user.profile?.fullName || user.username || "Anonymous"}
              initialsLength={2}
              imageUrl={user.profile?.image}
            />
            <EuiTitle size="l">
              <h2>@{user.username}</h2>
            </EuiTitle>
            <EuiText>
              <p>
                <EuiIcon type="email" /> {user.email}
              </p>
              <p>
                <EuiIcon type="clock" /> member since {moment(user.createdAt).format("DD-MM-YYYY")}
              </p>
              <p>
                <EuiIcon type="alert" />{" "}
                {user.profile?.fullName ? user.profile.fullName : "Full name not specified"}
              </p>
              <p>
                <EuiIcon type="number" />{" "}
                {user.profile?.phone ? user.profile.phone : "No phone number added"}
              </p>
              <EuiHorizontalRule />
              <p>
                <EuiIcon type="quote" />{" "}
                {user.profile?.description
                  ? user.profile.description
                  : "This user hasn't written a bio yet"}
              </p>
            </EuiText>
          </StyledEuiPageContentBody>
        </EuiPageContent>
      </EuiPageBody>
    </StyledEuiPage>
  )
}

export default connect((state) => ({ user: state.auth.user }))(ProfilePage)
