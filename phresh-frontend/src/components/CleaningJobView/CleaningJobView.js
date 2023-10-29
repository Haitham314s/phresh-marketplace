import {
  EuiAvatar,
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
import { useParams } from "react-router-dom"
import styled from "styled-components"
import { CleaningJobCard, NotFoundPage } from "../../components"
import { Actions as cleaningActions } from "../../redux/cleanings"

const StyledEuiPage = styled(EuiPage)`
  flex: 1;
`
const StyledFlexGroup = styled(EuiFlexGroup)`
  padding: 1rem;
`

function CleaningJobView({
  isLoading,
  cleaningError,
  currentCleaningJob,
  fetchCleaningJobById,
  clearCurrentCleaningJob
}) {
  const { cleaning_id } = useParams()

  React.useEffect(() => {
    if (cleaning_id) {
      fetchCleaningJobById({ cleaning_id })
    }

    return () => clearCurrentCleaningJob()
  }, [cleaning_id, fetchCleaningJobById, clearCurrentCleaningJob])

  if (isLoading) return <EuiLoadingSpinner size="xl" />
  if (!currentCleaningJob) return <EuiLoadingSpinner size="xl" />
  if (!currentCleaningJob?.name) return <NotFoundPage />

  return (
    <StyledEuiPage>
      <EuiPageBody component="section">
        <EuiPageContent verticalPosition="center" horizontalPosition="center" paddingSize="none">
          <StyledFlexGroup justifyContent="flexStart" alignItems="center">
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
          </StyledFlexGroup>

          <EuiPageContentBody>
            <CleaningJobCard cleaningJob={currentCleaningJob} />
          </EuiPageContentBody>
        </EuiPageContent>
      </EuiPageBody>
    </StyledEuiPage>
  )
}

export default connect(
  (state) => ({
    isLoading: state.cleanings.isLoading,
    cleaningError: state.cleanings.cleaningsError,
    currentCleaningJob: state.cleanings.currentCleaningJob
  }),
  {
    fetchCleaningJobById: cleaningActions.fetchCleaningJobById,
    clearCurrentCleaningJob: cleaningActions.clearCurrentCleaningJob
  }
)(CleaningJobView)
