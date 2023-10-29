import {
  EuiHeader,
  EuiHeaderLink,
  EuiHeaderSection,
  EuiHeaderSectionItem,
  EuiIcon,
} from "@elastic/eui";
import styled from "styled-components";

const LogoSection = styled(EuiHeaderLink)`
  padding: 0 2rem;
`;

export default function Navbar({ ...props }) {
  return (
    <EuiHeader style={props.style || {}}>
      <EuiHeaderSection>
        <EuiHeaderSectionItem css={{ borderRight: "1px" }}>
          <LogoSection href="/">
            <EuiIcon type="cloudDrizzle" color="#1E90FF" size="l" /> Phresh
          </LogoSection>
        </EuiHeaderSectionItem>
      </EuiHeaderSection>
    </EuiHeader>
  );
}
