# ABCD Records

## 1. Basic use cases and classes

Rounded nodes denote use cases. Rectangular nodes outside the boundary denote actors.

```mermaid
flowchart TD
    M[Member]
    C[Order processing clerk]
    subgraph S["ABCD Records"]
        P([Place order])
        V([Verify membership])
        O([Process order])
        Pay([Make payment])
    end
    M --- P
    M --- Pay
    C --- V
    C --- O
    P -.->|?include?| V
```

```mermaid
classDiagram
    class Member {
        +memberId
        +name
        +postalAddress
        +placeOrder()
        +makePayment()
    }
    class Order {
        +orderId
        +orderDate
        +status
        +calculateTotal()
        +record()
    }
    class OrderProcessingClerk {
        +employeeId
        +name
        +office
        +verifyMembership()
        +processOrder()
    }
    Member "1" -- "0..*" Order : places
    OrderProcessingClerk "1" -- "0..*" Order : processes
```

## 2. Membership, fulfillment, and settlement

Royal members receive a discount and priority processing. They may put unavailable items on backorder. A failed membership check produces an application before any order is accepted.

```mermaid
flowchart TD
    M[Member]
    R[Royal member]
    N[Non-member]
    C[Order processing clerk]
    D[Collection department clerk]
    subgraph S["ABCD Records"]
        P([Place order])
        V([Verify membership])
        A([Send membership application])
        O([Process order])
        I([Verify item availability])
        B([Order unavailable items])
        F([Apply discount])
        Inv([Print invoice])
        L([Print shipping list])
        Pay([Make payment])
        Save([Record order in daily file])
    end
    M --- P
    M --- Pay
    R --- B
    N --- A
    C --- O
    C --- V
    D --- Pay
    P -.->|?include?| V
    A -.->|?extend? non-member| V
    O -.->|?include?| I
    O -.->|?include?| Inv
    O -.->|?include?| L
    O -.->|?include?| Save
    F -.->|?extend? Royal| O
    B -.->|?extend? Royal and unavailable| I
```

```mermaid
classDiagram
    Member <|-- RoyalMember
    Member <|-- RegularMember
    Member "1" -- "0..*" Order : places
    OrderProcessingClerk "1" -- "0..*" Order : handles
    Order "1" *-- "1..*" OrderLine
    OrderLine "0..*" --> "1" Item
    Item <|-- CD
    Item <|-- Tape
    Order "1" -- "0..1" Invoice
    Order "1" -- "0..*" ShippingList
    ShippingList "0..*" -- "1..*" OrderLine : lists
    Order "1" -- "0..1" Payment
    Payment <|-- Cash
    Payment <|-- Check
    Payment <|-- BankDraft
    CollectionDepartmentClerk "1" -- "0..*" Payment : verifies
    DailyRecordsFile "1" -- "0..*" Order : records
    NonMember "1" -- "0..*" MembershipApplication : receives
    OrderProcessingClerk "1" -- "0..*" MembershipApplication : sends
    class RoyalMember {
        +discountRate
        +priority
    }
    class OrderLine {
        +quantity
        +unitPrice
        +backorderedQuantity
    }
```

## 3. Sequence diagrams

**Complete order.** A Royal member orders two different CDs, one copy of each, and pays by check. The deferred line stays on the same order for later shipment.

```mermaid
sequenceDiagram
    actor M as Royal member
    actor C as Order processing clerk
    participant S as ABCD Records
    actor D as Collection clerk
    M->>C: Order one copy each of CDs A and B
    C->>S: Verify membership and inventory
    S-->>C: Royal member, A available, B unavailable
    C->>S: Reserve A and backorder B
    C->>S: Apply Royal discount and priority
    S->>S: Save order and both lines in daily file
    S-->>C: Print discounted invoice and shipping list for A
    C-->>M: Send invoice and backorder notice
    M->>D: Pay invoice by check
    D->>S: Record check and confirm when cleared
    S-->>C: Release available CD for shipment
```

**Membership verification**

```mermaid
sequenceDiagram
    actor A as Applicant or member
    actor C as Order processing clerk
    participant S as ABCD Records
    A->>C: Submit order request
    C->>S: Look up membership
    alt Active Royal or Regular membership
        S-->>C: Return member ID and class
        C->>S: Create order
    else No active membership
        S-->>C: Provide membership form
        C-->>A: Mail application
    end
```

**Payment processing**

```mermaid
sequenceDiagram
    actor M as Member
    actor D as Collection clerk
    participant S as ABCD Records
    M->>D: Submit payment for invoice
    alt Cash
        D->>S: Confirm cash counted
    else Check
        D->>S: Record check pending clearance
        D->>S: Confirm cleared funds
    else Bank draft
        D->>S: Verify draft and confirm funds
    end
    S->>S: Match amount to invoice and record settlement
    S-->>M: Issue receipt
```

**Royal backorder fulfillment**

```mermaid
sequenceDiagram
    actor M as Member
    actor C as Order processing clerk
    participant S as ABCD Records
    participant Supplier
    C->>S: Check item and membership class
    alt Royal and unavailable
        C->>S: Record deferred quantity on order line
        S->>Supplier: Reorder missing units
        S-->>M: Confirm backorder
        Supplier-->>S: Deliver stock
        S->>S: Allocate stock to priority order
        S-->>C: Print remaining shipping list
        C-->>M: Ship item
    else Regular and unavailable
        C-->>M: Offer available items only
    end
```
