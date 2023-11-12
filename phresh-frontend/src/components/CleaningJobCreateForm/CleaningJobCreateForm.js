import {
  EuiButton,
  EuiFieldNumber,
  EuiFieldText,
  EuiForm,
  EuiFormRow,
  EuiSpacer,
  EuiSuperSelect,
  EuiTextArea
} from "@elastic/eui";
import { useCleaningJobForm } from "hooks/ui/useCleaningJobForm";
import React from "react";
import { connect } from "react-redux";
import { useNavigate } from "react-router-dom";
import { Actions as cleaningActions } from "redux/cleanings";

function CleaningJobCreateForm({ createCleaning }) {
  const navigate = useNavigate();
  const {
    form,
    errors,
    setErrors,
    isLoading,
    validateInput,
    setHasSubmitted,
    getFormErrors,
    cleaningTypeOptions,
    onCleaningTypeChange,
    onInputChange
  } = useCleaningJobForm();

  const handleSubmit = async (e) => {
    e.preventDefault();

    Object.keys(form).forEach((label) => validateInput(label, form[label]));

    if (!Object.values(form).every((value) => Boolean(value))) {
      setErrors((errors) => ({ ...errors, form: `You must fill out all fields.` }));
      return;
    }

    setHasSubmitted(true);

    const res = await createCleaning({ new_cleaning: { ...form } });
    if (res.success) {
      const cleaningId = res.data?.id;
      navigate(`/cleaning-jobs/${cleaningId}`);
    }
  };

  return (
    <>
      <EuiForm
        component="form"
        onSubmit={handleSubmit}
        isInvalid={Boolean(getFormErrors().length)}
        error={getFormErrors()}
      >
        <EuiFormRow
          label="Job Title"
          helpText="What do you want cleaners to see first?"
          isInvalid={Boolean(errors.name)}
          error={`Please enter a valid name.`}
        >
          <EuiFieldText
            name="name"
            value={form.name}
            onChange={(e) => onInputChange(e.target.name, e.target.value)}
          />
        </EuiFormRow>

        <EuiFormRow label="Select a cleaning type">
          <EuiSuperSelect
            options={cleaningTypeOptions}
            valueOfSelected={form.cleaning_type}
            onChange={(value) => onCleaningTypeChange(value)}
            itemLayoutAlign="top"
            hasDividers
          />
        </EuiFormRow>

        <EuiFormRow
          label="Hourly Rate"
          helpText="List a reasonable price for each hour of work the employee logs."
          isInvalid={Boolean(errors.price)}
          error={`Price should match the general format: 9.99`}
        >
          <EuiFieldNumber
            name="price"
            icon="currency"
            placeholder="19.99"
            value={form.price}
            onChange={(e) => onInputChange(e.target.name, e.target.value)}
          />
        </EuiFormRow>

        <EuiFormRow
          label="Job Description"
          helpText="What do you want prospective employees to know about this opportunity?"
          isInvalid={Boolean(errors.description)}
          error={`Please enter a valid input.`}
        >
          <EuiTextArea
            name="description"
            placeholder="I'm looking for..."
            value={form.description}
            onChange={(e) => onInputChange(e.target.name, e.target.value)}
          />
        </EuiFormRow>

        <EuiSpacer />

        <EuiButton type="submit" isLoading={isLoading} fill>
          Create Cleaning
        </EuiButton>
      </EuiForm>
    </>
  );
}

export default connect(null, {
  createCleaning: cleaningActions.createCleaningJob
})(CleaningJobCreateForm);
