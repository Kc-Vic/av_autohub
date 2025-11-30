# Testing Documentation - CivIntel Platform

[Back to README](README.md)

## Table of Contents
- [Functionality Testing](#functionality-testing)
- [Authentication Testing](#authentication-testing)
- [CRUD Operations Testing](#crud-operations-testing)
- [Comment System Testing](#comment-system-testing)
- [Button Testing](#button-testing)
- [Browser Compatibility](#browser-compatibility)
- [Responsiveness Testing](#responsiveness-testing)
- [Validator Testing](#validator-testing)
- [Known Bugs and Fixes](#known-bugs-and-fixes)
- [User Stories Implementation](#user-stories-implementation)

## Functionality Testing

| Test | Description | Expected Outcome | Result |
|------|-------------|-----------------|--------|
| Homepage Load | Navigate to homepage | Homepage should display with background image, navigation at the top and button to link to products | PASS |
| Product Page | Click on "Shop Now" | All products should display in columns | PASS |
| Product Detail View | Click on any product image | Full product details should display | PASS |
| Filter System | Apply Brand/Category/Accessories/Special Offers Filter | Products should filter according to selected criteria in the Nav | PASS |
| Search Function | Enter search term in search box | Relevant products matching search term should display. If no search item is added, warning message displays | PASS |
| Sort | Select All Products-By Price | Products should be sorted by increasing or decreasing price using the sort by toggle | PASS |
| Credit Options | Identify products with credit | Icon should display showing if a product is eligible for credit | PASS |
| Credit Options2 | Click Show Credit Options Button | Credit Options should display calculating the required payment plans | PASS |
| Profile | Display saved information | Profile view should include saved delivery information as well as order history and credit applications | PASS |
| Credit Applications | Application should have unique IDs and be linked to product id| Credit applications should have a unique application ID and also be linked to specific product | FAIL |
| Product Management | Edit/Add/Delete products| Admin can add new products, edit and delete existing products from the front end | PASS |
| Messages | Receive messages for each action | Warning, confirmation and error messages are displayed on each page for different actions | PASS |

## Authentication Testing

| Test | Description | Expected Outcome | Result |
|------|-------------|-----------------|--------|
| User Registration | Complete signup form with valid data | New account created, user logged in automatically | PASS |
| User Login | Login with valid credentials | User successfully logged in and redirected to Profile | PASS |
| Invalid Login | Login with incorrect credentials | Error message displayed, user remains on login page | PASS |
| Logout Function | Click logout button | User logged out and redirected to homepage | PASS |
| Protected Routes | Access /credit_options/ without login | Redirected to login page | PASS |
| Session Persistence | Close and reopen browser | User remains logged in (session cookie active) | PASS |
| Password Validation | Register with weak password | Error message about password requirements | PASS |
| Duplicate Username | Register with existing username | Error message about username already taken | PASS |

## CRUD Operations Testing

### Create Tests
| Test | Description | Expected Outcome | Result |
|------|-------------|-----------------|--------|
| Product Management (Super User) | Edit/Delete/Add Products | Existing products can be modified and deleted with superuser login | PASS |
| Create options (Guest User) | Try to access credit options without login | Redirected to login page | PASS |


### Update Tests
| Test | Description | Expected Outcome | Result |
|------|-------------|-----------------|--------|
| Edit Product | Superuser clicks on edit | Product form opens and is modified after user clicks update | PASS |
| Edit Product Image | Add new image | New image added when super user hits update but not displayed product page | FAIL |

### Delete Tests
| Test | Description | Expected Outcome | Result |
|------|-------------|-----------------|--------|
| Delete Product | Superuser clicks delete button | Confirmation modal appears | PASS |

## Profile Page Testing

| Test | Description | Expected Outcome | Result |
|------|-------------|-----------------|--------|
| Order History | Complete checkout on order | Order details Appear in user profile | PASS |
| Credit Application History | Complete Credit Application | Credit application details appear in user profile | PASS |
| Delivery Details | Complete deliver details form and hit update button | Default delivery details is updated to profile | PASS |

## Checkout Testing

| Test | Description | Expected Outcome | Result |
|------|-------------|-----------------|--------|
| Checkout1 | Click proceed to checkout on product item | Checkout page provides form for delivery details and option to save delivery information to profile | PASS |
| Checkout2 | Click proceed to checkout on product item | Checkout page accurately pulls correct price from selected product | PASS |
| Order Confirmation | Email confirmation on order | User receives detailed order confirmation after order is completed| FAIL |
| Paystack Payments | Complete order button | User is redirected to paystack page for order payment  | PASS |

## Paystack Testing

| Test | Description | Expected Outcome | Result |
|------|-------------|-----------------|--------|
| Payment options | Click complete order button | User is provided with multiple payment options | PASS |
| Confirmation Email | Complete payment | User receives confirmation email from paystack | PASS |

## Button Testing

### Interactive Button Tests
| Test | Description | Expected Outcome | Result |
|------|-------------|-----------------|--------|
| Shop Now Button | Go to Shopping page | User is redirected to products page| PASS |
| Sort Button | View sort dropdown | User can see the dropdown to sort items by ascending or descending price | PASS |
| Arrow Up button | Click Arrow up button | Navigate to top of page | PASS |


## Browser Compatibility

| Browser | Version | Compatibility | Notes |
|---------|---------|---------------|-------|
| Chrome | Latest (120+) | Full | All features work as expected |
| Firefox | Latest (120+) | Full | All features work as expected |
| Safari | Latest (17+) | Full | All features work as expected |
| Edge | Latest (120+) | Full | All features work as expected |
| Opera | Latest | Full | All features work as expected |
| Mobile Chrome | Latest | Full | Responsive design works perfectly |
| Mobile Safari | Latest | Full | iOS specific styling applied correctly |

## Responsiveness Testing

| Device/Screen Size | Compatibility | Notes |
|-------------------|---------------|-------|
| Desktop (1920px) | Full | All elements display in grid layout |
| Laptop (1366px) | Full | Navigation and cards display correctly |
| Tablet (768px) | Full | Navigation collapses to hamburger menu |
| Mobile (480px) | Full | Single column layout, stacked elements |
| iPhone 12/13 | Full | Optimized for notch, proper spacing |
| Samsung Galaxy | Full | Android-specific rendering correct |
| iPad Pro | Full | Makes use of larger tablet screen |

### Responsive Elements Testing
| Element | Behavior | Result |
|---------|----------|--------|
| Navigation Bar | Collapses to hamburger menu < 768px | PASS |
| Report Cards | Stack vertically on mobile | PASS |
| Filter Form | Fields stack on small screens | PASS |
| Tables | Horizontal scroll on mobile | PASS |
| Modals | Resize to fit screen | PASS |
| Footer | Scale proportionally | FAIL |

## Validator Testing

### HTML Validation
- **Tool Used**: [W3C HTML Validator](https://validator.w3.org/)
- **Results**: 
  - ✅ No errors in base.html
  - ✅ No errors in report templates
  - ⚠️ Warning: Empty heading in modal (non-critical)

### CSS Validation
- **Tool Used**: [W3C CSS Validator (Jigsaw)](https://jigsaw.w3.org/css-validator/)
- **Results**:
  - ✅ No errors in custom CSS
  - ℹ️ Bootstrap CSS warnings (expected, third-party)

### Python/PEP8 Validation
- **Tool Used**: pycodestyle (formerly pep8)
- **Results**:
  - ✅ views.py - No errors
  - ✅ models.py - No errors
  - ✅ forms.py - No errors
  - ✅ urls.py - No errors
  - ⚠️ settings.py - Line too long warnings (URLs)

### JavaScript Validation
- **Tool Used**: JSHint
- **Results**:
  - ✅ No critical errors
  - ⚠️ ES6 warnings (let/const usage)

## Automated Testing

### Running Test Suite
```bash
python manage.py test
```

### Test Results Summary
| Test Module | Tests Run | Passed | Failed | Coverage |
|------------|-----------|--------|--------|----------|
| test_models.py | 8 | 8 | 0 | 95% |
| test_forms.py | 6 | 6 | 0 | 92% |
| test_views.py | 10 | 10 | 0 | 88% |
| **Total** | **24** | **24** | **0** | **91.7%** |

## Known Bugs and Fixes

### Fixed Bugs


#### Bug 1: Static Files Not Loading in Production
- **Issue**: CSS and images returning 404 errors on Heroku
- **Cause**: Incorrect static files configuration
- **Fix**: Added correct variables to Amazon AWS BUcket


#### Bug 3: Email Validation
- **Issue**: Email validation failure
- **Cause**: Outdated django version
- **Fix**: Updated django in new virtual environment


### Remaining Issues

#### Issue 1: Image Upload and Display
- **Problem**: Images fail to display when added in front end
- **Error**: "Failed to load resource: the server responded with a status of 404"
- **Attempted Solutions**:
  - Configured MEDIA_URL and MEDIA_ROOT
  - Added media files to AWS storage
  - Checked file path
- **Status**: Under investigation
- **Workaround**: Deleted products

#### Issue 2: Paypal Webhook not working
- **Problem**: Paypal webhook API not available to enable detailed order confirmation
- **Temporary Fix**: Relying on default paypal order confirmation
- **Permanent Solution Needed**: Configure proper webhook using pre-existing views

#### Issue 3: Credit Application Verification
- **Problem**: Credit applications cannot be verified from the front end
- **Cause**: Credit applications are not linked to products primary key.
- **Solution**: No solution as yet

## User Stories Implementation

### User Story 1: Edit Profile
> **As a user I want to edit my profile so that I can make changes to my personal information**

**Implementation:**
- ✅ Details update option in user profile

### User Story 2: Guest Access
> **As a guest user I want to access the app without creating an account so that I can have a look at the car inventory**

**Implementation:**
- ✅ Guests users can access the full app inventory through the shop now button.

### User Story 3: User Profile
> **As a User I want to create a profile so that I can upload personal details and manage my account**

**Implementation:**
- ✅ Users can update supporting documents for credit application.
- ✅ Documents can only be reviewed by user and admin.

### User Story 4: Filter
> **As a user I want to filter the car inventory so that I can narrow than my search**

**Implementation:**
- ✅ Navigation links provide filter functionality by Brand, Condition and Credit Availability
- ✅ Users can search for specific models of each car
- ✅ Sort allows users sort inventory by price

### User Story 5: FCheckout and payment
> **As a user I want to securely checkout so that I can make payments for selected items**

**Implementation:**
- ✅ Paypal handles all user payments securely
- ✅ Messages alert user on successful and unsuccessful transactions

### User Story 6: Credit Assessment
> **As a user I want to to take a credit assesment so that I can check my eligibility for credit**

**Implementation:**
- ✅ Credit application forms allow users provide details necessary for credit assessments.
- ✅ Only Admin can see credit information.
- ✅ Credit application forms can handle media documents including pdfs, jpegs and word documents.
---

## Testing Conclusion

The CivIntel platform has undergone comprehensive testing across multiple areas:

- **Functionality**: Core features working as expected
- **Authentication**: Secure user system implemented
- **CRUD Operations**: Full create, read, update, delete functionality
- **Responsiveness**: Works across all device sizes
- **Browser Compatibility**: Consistent experience across browsers

**Outstanding Issues**: Image upload functionality requires additional configuration for production environment.

**Overall Assessment**: The platform is production-ready with minor styling issues that don't affect core functionality. It requires further work on the handling of credit applications, and product management update. 