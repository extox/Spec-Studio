# Create IaC Workflow

## Overview
Produce a vendor-neutral Infrastructure-as-Code sketch in YAML, covering every
deployable resource derived from the architecture. The artifact is trivially
translatable to Terraform, AWS CDK, Azure Bicep, or Pulumi.

The output file is saved under `construction-artifacts/iac.yaml`.

## Step-by-Step Instructions

### Step 1: Load Architecture
**Goal:** Confirm target cloud and component list.

- Load `planning-artifacts/architecture.md` and `tech-stack` context.
- Ask the user to confirm the target cloud: AWS / GCP / Azure / on-prem / multi.
- List every architecture component (C-1, C-2, ...) that maps to a real
  runtime resource.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 2: Resource Inventory
**Goal:** Enumerate every resource the system needs.

- Compute: VMs / containers / functions / managed runtimes.
- Storage: object store / block / file / DB.
- Network: VPC / subnets / load balancers / CDN / DNS.
- Identity: service accounts / IAM roles / policies.
- Secrets & config: secret stores, parameter stores.
- Each resource: `id | type | component (C-#) | env (dev/staging/prod)`.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 3: Dependencies
**Goal:** Capture the order resources must be created in.

- Draw dependency edges: "Resource A depends_on Resource B".
- Flag any circular dependency and resolve it.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 4: Network Topology
**Goal:** Define the network containment.

- VPC / VNet boundaries.
- Public vs private subnets.
- Security groups / NSGs / firewall rules (allow-list, never deny-all-then-allow chains).

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 5: Secrets & Config
**Goal:** List secrets without leaking them.

- Secrets table: `name | consumer | store | rotation policy`.
- Config values per environment.
- ALWAYS use placeholders like `${{ secrets.DB_PASSWORD }}` — NEVER plaintext.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

### Step 6: Save IaC
**Goal:** Produce and save the final iac artifact.

- Use the `iac` YAML template.
- Add `<!-- derived_from: ARCH#C-{n} -->` comment blocks above each resource
  block that maps to a specific architecture component.
- Wrap in `<!-- SAVE_FILE: construction-artifacts/iac.yaml -->` and
  `<!-- END_FILE -->`.

**Menu:** [A] Advanced Elicitation | [P] Party Mode | [C] Continue

## Completion
After saving, suggest next steps:
- Translate iac.yaml to the actual IaC language for the target cloud.
- Pair with the CI pipeline so deploys become repeatable.
