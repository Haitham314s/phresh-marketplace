import {
  EuiAvatar,
  EuiButtonEmpty,
  EuiButtonIcon,
  EuiFlexGroup,
  EuiFlexItem,
  EuiLoadingSpinner,
  EuiPage,
  EuiPageBody,
  EuiPageContent,
  EuiPageContentBody,
  EuiTitle
} from "@elastic/eui"
import React from "react"
import { connect } from "react-redux"
import { Route, Routes, useNavigate, useParams } from "react-router-dom"
import styled from "styled-components"
import {
  CleaningJobCard,
  CleaningJobEditForm,
  NotFoundPage,
  PermissionsNeeded
} from "../../components"
import { Actions as cleaningActions } from "../../redux/cleanings"
import { Actions as offersActions } from "../../redux/offers"

const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`
const StyledFlexGroup = styled(EuiFlexGroup)`
  padding: 1rem;
`

function CleaningJobView({
  user,
  isLoading,
  offersError,
  cleaningError,
  offersIsLoading,
  currentCleaningJob,
  fetchCleaningJobById,
  createOfferForCleaning,
  clearCurrentCleaningJob,
  fetchUserOfferForCleaningJob
}) {
  const { cleaning_id } = useParams()
  const navigate = useNavigate()

  const userOwnsCleaningResource = user?.username && currentCleaningJob?.owner?.id === user?.id

  React.useEffect(() => {
    if (cleaning_id && user?.username) {
      fetchCleaningJobById({ cleaning_id })

      if (!userOwnsCleaningResource) {
        fetchUserOfferForCleaningJob({ cleaning_id, username: user.username })
      }
    }

    return () => clearCurrentCleaningJob()
  }, [
    cleaning_id,
    fetchCleaningJobById,
    clearCurrentCleaningJob,
    userOwnsCleaningResource,
    fetchUserOfferForCleaningJob,
    user
  ])

  React.useEffect(() => {
    if (cleaning_id) {
      fetchCleaningJobById({ cleaning_id })
    }

    return () => clearCurrentCleaningJob()
  }, [cleaning_id, fetchCleaningJobById, clearCurrentCleaningJob])

  if (isLoading) return <EuiLoadingSpinner size="xl" />
  if (!currentCleaningJob) return <EuiLoadingSpinner size="xl" />
  if (!currentCleaningJob?.name) return <NotFoundPage />

  const editJobButton = userOwnsCleaningResource ? (
    <EuiButtonIcon iconType="documentEdit" aria-label="edit" onClick={() => navigate(`edit`)} />
  ) : null
  const goBackButton = (
    <EuiButtonEmpty
      iconType="sortLeft"
      size="s"
      onClick={() => navigate(`/cleaning-jobs/${currentCleaningJob.id}`)}
    >
      back to job
    </EuiButtonEmpty>
  )

  const viewCleaningJobElement = (
    <CleaningJobCard
      user={user}
      offersError={offersError}
      cleaningJob={currentCleaningJob}
      offersIsLoading={offersIsLoading}
      isOwner={userOwnsCleaningResource}
      createOfferForCleaning={createOfferForCleaning}
    />
  )
  const editCleaningJobElement = (
    <PermissionsNeeded
      element={<CleaningJobEditForm cleaningJob={currentCleaningJob} />}
      isAllowed={userOwnsCleaningResource}
    />
  )

  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <EuiPageContent verticalPosition="center" horizontalPosition="center" paddingSize="none">
          <StyledFlexGroup alignItems="center" direction="row" responsive={false}>
            <EuiFlexItem>
              <EuiFlexGroup
                justifyContent="flexStart"
                alignItems="center"
                direction="row"
                responsive={false}
              >
                <EuiFlexItem grow={false}>
                  <EuiAvatar
                    size="xl"
                    name={
                      currentCleaningJob.owner?.profile?.full_name ||
                      currentCleaningJob.owner?.username ||
                      "Anonymous"
                    }
                    initialsLength={2}
                    imageUrl={currentCleaningJob.owner?.profile?.image}
                  />
                </EuiFlexItem>
                <EuiFlexItem>
                  <EuiTitle>
                    <p>@{currentCleaningJob.owner?.username}</p>
                  </EuiTitle>
                </EuiFlexItem>
              </EuiFlexGroup>
            </EuiFlexItem>
            <EuiFlexItem grow={false}>
              <Routes>
                <Route path="/" element={editJobButton} />
                <Route path="/edit" element={goBackButton} />
              </Routes>
            </EuiFlexItem>
          </StyledFlexGroup>

          <EuiPageContentBody>
            <Routes>
              <Route path="/" element={viewCleaningJobElement} />
              <Route path="/edit" element={editCleaningJobElement} />
              <Route path="*" element={<NotFoundPage />} />
            </Routes>
          </EuiPageContentBody>
        </EuiPageContent>
      </EuiPageBody>
    </StyledEuiPage>
  )
}

export default connect(
  (state) => ({
    user: state.auth.user,
    isLoading: state.cleanings.isLoading,
    offersIsLoading: state.offers.isLoading,
    offersError: state.offers.error,
    cleaningError: state.cleanings.cleaningsError,
    currentCleaningJob: state.cleanings.currentCleaningJob
  }),
  {
    fetchCleaningJobById: cleaningActions.fetchCleaningJobById,
    clearCurrentCleaningJob: cleaningActions.clearCurrentCleaningJob,
    fetchUserOfferForCleaningJob: offersActions.fetchUserOfferForCleaningJob,
    createOfferForCleaning: offersActions.createOfferForCleaning
  }
)(CleaningJobView)
