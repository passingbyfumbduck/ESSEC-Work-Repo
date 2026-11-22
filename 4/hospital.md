# Hospital management

## 1. Staff and patient roles

Each case has one coordinator. A patient and a doctor can each work with several coordinators across different cases.

```mermaid
classDiagram
    class Patient {
        +memberId
        +name
        +email
        +submitProblem()
        +receivePrescription()
        +pay()
    }
    class Organizer {
        +staffId
        +name
        +email
        +consultDoctor()
        +deliverPrescription()
        +forwardPayment()
    }
    class Doctor {
        +licenseNumber
        +name
        +specialty
        +reviewProblem()
        +prescribe()
        +receivePayment()
    }
    Patient "0..*" -- "0..*" Organizer : contacts
    Organizer "0..*" -- "0..*" Doctor : consults
```

## 2. Cases, prescriptions, and payments

```mermaid
classDiagram
    Patient "1" -- "0..*" HealthProblem : submits
    Organizer "1" -- "0..*" HealthProblem : coordinates
    Doctor "0..*" -- "0..*" HealthProblem : reviews
    HealthProblem "1" *-- "0..*" Prescription
    Doctor "1" -- "0..*" Prescription : writes
    Prescription "1" -- "0..1" Payment : settles
    Patient "1" -- "0..*" Payment : makes
    Organizer "1" -- "0..*" Payment : forwards
    Doctor "1" -- "0..*" Payment : receives
    class HealthProblem {
        +caseId
        +description
        +status
        +submittedAt
    }
    class Prescription {
        +prescriptionId
        +instructions
        +issuedAt
        +deliveredAt
    }
    class Payment {
        +paymentId
        +amount
        +method
        +status
    }
```

A payment method is Check, Cash, or CreditCard. The advanced model below supplies its behavior.

```mermaid
sequenceDiagram
    actor P as Patient
    participant O as Organizer
    participant D as Doctor
    P->>O: Submit health problem
    O->>D: Request consultation
    D-->>O: Return signed prescription
    O-->>P: Deliver prescription and amount due
    P->>O: Pay by selected method
    O->>D: Forward settled payment
    O-->>P: Send receipt
```

## 3. Shared identity, case history, and payment strategy

The diagrams below extend the case model. A case starts pending, moves to in-review at consultation, and becomes resolved when the organizer delivers the prescription. The case keeps its submission, review, and resolution times. A doctor can reference earlier prescriptions for the same patient while issuing a new dated record.

```mermaid
classDiagram
    class User {
        <<abstract>>
        +id
        +name
        -passwordHash
        +login()
        +logout()
    }
    User <|-- Patient
    User <|-- Doctor
    User <|-- Organizer
    class Organizer {
        +issueMemberCredentials()
        +maintainDatabase()
        +updateSystem()
    }
    class HealthProblem {
        +submittedAt
        +reviewedAt
        +resolvedAt
    }
    Prescription "0..*" --> "0..*" Prescription : cites earlier
```

```mermaid
classDiagram
    Payment "0..*" --> "1" PaymentStrategy : uses
    class PaymentStrategy {
        <<interface>>
        +collect(amount)
    }
    PaymentStrategy <|.. Check
    PaymentStrategy <|.. Cash
    PaymentStrategy <|.. CreditCard
    class Payment {
        +idempotencyKey
        +settledAt
        +forwardedAt
        +collect()
        +forward()
    }
```

**Registration**

```mermaid
sequenceDiagram
    actor P as Patient
    actor O as Organizer
    participant S as Hospital system
    P->>O: Request membership
    O->>S: Register new member
    S-->>O: Return member ID and one-time activation instructions
    O-->>P: Deliver credentials
    P->>S: Activate account and choose password
    S-->>P: Confirm registration
```

**Consultation**

```mermaid
sequenceDiagram
    actor P as Patient
    participant S as Hospital system
    actor O as Organizer
    actor D as Doctor
    P->>S: Submit problem
    S-->>O: Notify of pending case
    O->>S: Review and assign doctor
    S-->>D: Request consultation and show patient history
    D->>S: Issue dated prescription for case
    S-->>O: Notify prescription ready
    O->>S: Release prescription
    S-->>P: Deliver prescription and mark case resolved
```

**Payment**

```mermaid
sequenceDiagram
    actor P as Patient
    participant S as Hospital system
    actor O as Organizer
    actor D as Doctor
    P->>S: Pay for prescription using chosen method
    alt Payment settles
        S-->>P: Return receipt
        S-->>O: Show settlement ready to forward
        O->>S: Forward settlement
        S-->>D: Confirm payment
    else Declined or awaiting clearance
        S-->>P: Report status
    end
```

Multiple doctors can review a case. Each prescription identifies the doctor who signed it, which also identifies the payee. Prior prescriptions are reusable as references, with amendments recorded as new prescriptions. Payment uses the Strategy pattern. Check payments wait for clearance. A unique request key prevents duplicate collection, and one forwarding record per settled payment prevents a second payout. The system records each change of status and its timestamp in the same transaction as its ledger entry.
