$('document').ready(function () {
    function onCategoryUploadChange() {
        var category = $('#category_upload').val();

        $('#sm_category_upload').prop('disabled', false);
        var select = document.getElementById('sm_category_upload');
        select.innerHTML = '<option value="">Select Sub-sub Category</option>';

        var select = document.getElementById('md_category_upload');
        select.innerHTML = '<option value="">Select Sub Category</option>';

        if (category === "") {
            return;
        }


        if (category === "Official Common Templates") {
            var option = document.createElement('option');
            option.value = "Program Template";
            option.innerText = "Program Template";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Contract Template";
            option.innerText = "Contract Template";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Staff Report Template";
            option.innerText = "Staff Report Template";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Others";
            option.innerText = "Others";
            select.append(option);
        }
        else if (category === "HR & Administration Management") {
            var option = document.createElement('option');
            option.value = "Hiring Template";
            option.innerText = "Hiring Template";
            select.append(option);

            var option = document.createElement('option');
            option.value = "VI System";
            option.innerText = "VI System";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Finance & Payroll";
            option.innerText = "Finance & Payroll";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Staff Documentation";
            option.innerText = "Staff Documentation";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Company Documentation";
            option.innerText = "Company Documentation";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Tax History";
            option.innerText = "Tax History";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Invoice History";
            option.innerText = "Invoice History";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Others";
            option.innerText = "Others";
            select.append(option);
        }
        else if (category === "Promotional&Design Materials") {
            var option = document.createElement('option');
            option.value = "Wording and PPT";
            option.innerText = "Wording and PPT";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Pictures";
            option.innerText = "Pictures";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Videos";
            option.innerText = "Videos";
            select.append(option);

            var option = document.createElement('option');
            option.value = "BGE Partner High Schools";
            option.innerText = "BGE Partner High Schools";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Others";
            option.innerText = "Others";
            select.append(option);
        }
        else if (category === "Program & Student Information") {
            var option = document.createElement('option');
            option.value = "High School Program";
            option.innerText = "High School Program";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Camp Program";
            option.innerText = "Camp Program";
            select.append(option);

            var option = document.createElement('option');
            option.value = "College Counseling Program";
            option.innerText = "College Counseling Program";
            select.append(option);

            var option = document.createElement('option');
            option.value = "ESL Teacher Recruitment Program";
            option.innerText = "ESL Teacher Recruitment Program";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Likeshuo Program";
            option.innerText = "Likeshuo Program";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Others";
            option.innerText = "Others";
            select.append(option);
        }
        else {
            var option = document.createElement('option');
            option.value = "Previous Staff Documentation";
            option.innerText = "Previous Staff Documentation";
            select.append(option);
        }
    }

    function onMiddleCategoryUploadChange() {
        var category = $('#category_upload').val();
        var mdCategory = $('#md_category_upload').val();

        $('#sm_category_upload').prop('disabled', false);
        var select = document.getElementById('sm_category_upload');
        select.innerHTML = '<option value="">Select Sub-sub Category</option>';

        if (category === "" || mdCategory === "") {
            return;
        }


        if (category === "Official Common Templates") {
            if (mdCategory === "Program Template") {
                var option = document.createElement('option');
                option.value = "High School Program Template";
                option.innerText = "High School Program Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Camp Program Template";
                option.innerText = "Camp Program Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "College Couseling Template";
                option.innerText = "College Couseling Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "ESL Teacher Recruitment";
                option.innerText = "ESL Teacher Recruitment";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Likeshuo Program Template";
                option.innerText = "Likeshuo Program Template";
                select.append(option);
            }
            else if (mdCategory === "Contract Template") {
                var option = document.createElement('option');
                option.value = "High School Program Contract Template";
                option.innerText = "High School Program Contract Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Camp Program Contract Template";
                option.innerText = "Camp Program Contract Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "College Counseling Program Contract Template";
                option.innerText = "College Counseling Program Contract Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "ESL Teacher Recruitement Contract Template";
                option.innerText = "ESL Teacher Recruitement Contract Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Likeshuo Program Contract Template";
                option.innerText = "Likeshuo Program Contract Template";
                select.append(option);
            }
            else if (mdCategory === "Staff Report Template") {
                var option = document.createElement('option');
                option.value = "Office Weekly Meeting Report Template";
                option.innerText = "Office Weekly Meeting Report Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Businesss Trip Report";
                option.innerText = "Businesss Trip Report";
                select.append(option);
            }
            else {
                // Others
                $('#sm_category_upload').prop('disabled', true);
                var select = document.getElementById('sm_category_upload');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
        }
        else if (category === "HR & Administration Management") {
            if (mdCategory === "Hiring Template") {
                var option = document.createElement('option');
                option.value = "Job Offer Letter Template";
                option.innerText = "Job Offer Letter Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Employment Agreement Template";
                option.innerText = "Employment Agreement Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Performance Review Form Template";
                option.innerText = "Performance Review Form Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Employee Exit Memo Template";
                option.innerText = "Employee Exit Memo Template";
                select.append(option);
            }
            else if (mdCategory === "VI System") {
                var option = document.createElement('option');
                option.value = "Company Logo";
                option.innerText = "Company Logo";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Letter Head";
                option.innerText = "Letter Heade";
                select.append(option);

                var option = document.createElement('option');
                option.value = "PPT Template";
                option.innerText = "PPT Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Email Signature";
                option.innerText = "Email Signature";
                select.append(option);
            }
            else if (mdCategory === "Finance & Payroll") {
                var option = document.createElement('option');
                option.value = "Doposit Authorization";
                option.innerText = "Doposit Authorizationo";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Expense Report";
                option.innerText = "Expense Report";
                select.append(option);
            }
            else if (mdCategory === "Staff Documentation") {
                // Employee name_yyyy
                $('#sm_category_upload').prop('disabled', true);
                var select = document.getElementById('sm_category_upload');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
            else if (mdCategory === "Company Documentation") {
                var option = document.createElement('option');
                option.value = "Business License";
                option.innerText = "Business License";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Company Bank Information";
                option.innerText = "Company Bank Information";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Office Lease Agreement";
                option.innerText = "Office Lease Agreement";
                select.append(option);

                var option = document.createElement('option');
                option.value = "CSIET";
                option.innerText = "CSIET";
                select.append(option);

                var option = document.createElement('option');
                option.value = "BGE Manuel";
                option.innerText = "BGE Manuel";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Contract and Agreement";
                option.innerText = "Contract and Agreement";
                select.append(option);
            }
            else if (mdCategory === "Tax History") {
                // Tax History
                $('#sm_category_upload').prop('disabled', true);
                var select = document.getElementById('sm_category_upload');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
            else if (mdCategory === "Invoice History") {
                // Invoice History
                $('#sm_category_upload').prop('disabled', true);
                var select = document.getElementById('sm_category_upload');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
            else {
                // Others
                $('#sm_category_upload').prop('disabled', true);
                var select = document.getElementById('sm_category_upload');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
        }
        else if (category === "Promotional&Design Materials") {
            if (mdCategory === "Wording and PPT") {
                var option = document.createElement('option');
                option.value = "High School Program";
                option.innerText = "High School Program";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Camp";
                option.innerText = "Camp";
                select.append(option);

                var option = document.createElement('option');
                option.value = "College Couseling";
                option.innerText = "College Couseling";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Esl Teacher Recruitment";
                option.innerText = "Esl Teacher Recruitment";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Likeshuo";
                option.innerText = "Likeshuo";
                select.append(option);

                var option = document.createElement('option');
                option.value = "School Profile & Picture";
                option.innerText = "School Profile & Picture";
                select.append(option);
            }
            else if (mdCategory === "Pictures") {
                var option = document.createElement('option');
                option.value = "High School Program";
                option.innerText = "High School Program";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Camp";
                option.innerText = "Camp";
                select.append(option);

                var option = document.createElement('option');
                option.value = "College Couseling";
                option.innerText = "College Couseling";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Esl Teacher Recruitment";
                option.innerText = "Esl Teacher Recruitment";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Likeshuo";
                option.innerText = "Likeshuo";
                select.append(option);
            }
            else if (mdCategory === "Videos") {
                var option = document.createElement('option');
                option.value = "High School Program";
                option.innerText = "High School Program";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Camp";
                option.innerText = "Camp";
                select.append(option);

                var option = document.createElement('option');
                option.value = "College Couseling";
                option.innerText = "College Couseling";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Esl Teacher Recruitment";
                option.innerText = "Esl Teacher Recruitment";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Likeshuo";
                option.innerText = "Likeshuo";
                select.append(option);
            }
            else if (mdCategory === "BGE Partner High Schools") {
                var option = document.createElement('option');
                option.value = "Massachuessetts";
                option.innerText = "Massachuessetts";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Connecticut";
                option.innerText = "Connecticut";
                select.append(option);

                var option = document.createElement('option');
                option.value = "New Jersey";
                option.innerText = "New Jersey";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Pennsylvania";
                option.innerText = "Pennsylvania";
                select.append(option);

                var option = document.createElement('option');
                option.value = "California";
                option.innerText = "California";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Virginia";
                option.innerText = "Virginia";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Boarding Schools";
                option.innerText = "Boarding Schools";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Colleges";
                option.innerText = "Colleges";
                select.append(option);
            }
            else {
                // Others
                $('#sm_category_upload').prop('disabled', true);
                var select = document.getElementById('sm_category_upload');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
        }
        else if (category === "Program & Student Information") {
            $('#sm_category_upload').prop('disabled', true);
            var select = document.getElementById('sm_category_upload');
            select.innerHTML = '<option value="">Nothing..</option>';
        }
        else {
            $('#sm_category_upload').prop('disabled', true);
            var select = document.getElementById('sm_category_upload');
            select.innerHTML = '<option value="">Nothing..</option>';
        }
    }


    function onCategorySearchChange() {
        var category = $('#category_search').val();

        $('#sm_category_search').prop('disabled', false);
        var select = document.getElementById('sm_category_search');
        select.innerHTML = '<option value="">Select Sub-sub Category</option>';

        var select = document.getElementById('md_category_search');
        select.innerHTML = '<option value="">Select Sub Category</option>';

        if (category === "") {
            return;
        }


        if (category === "Official Common Templates") {
            var option = document.createElement('option');
            option.value = "Program Template";
            option.innerText = "Program Template";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Contract Template";
            option.innerText = "Contract Template";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Staff Report Template";
            option.innerText = "Staff Report Template";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Others";
            option.innerText = "Others";
            select.append(option);
        }
        else if (category === "HR & Administration Management") {
            var option = document.createElement('option');
            option.value = "Hiring Template";
            option.innerText = "Hiring Template";
            select.append(option);

            var option = document.createElement('option');
            option.value = "VI System";
            option.innerText = "VI System";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Finance & Payroll";
            option.innerText = "Finance & Payroll";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Staff Documentation";
            option.innerText = "Staff Documentation";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Company Documentation";
            option.innerText = "Company Documentation";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Tax History";
            option.innerText = "Tax History";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Invoice History";
            option.innerText = "Invoice History";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Others";
            option.innerText = "Others";
            select.append(option);
        }
        else if (category === "Promotional&Design Materials") {
            var option = document.createElement('option');
            option.value = "Wording and PPT";
            option.innerText = "Wording and PPT";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Pictures";
            option.innerText = "Pictures";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Videos";
            option.innerText = "Videos";
            select.append(option);

            var option = document.createElement('option');
            option.value = "BGE Partner High Schools";
            option.innerText = "BGE Partner High Schools";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Others";
            option.innerText = "Others";
            select.append(option);
        }
        else if (category === "Program & Student Information") {
            var option = document.createElement('option');
            option.value = "High School Program";
            option.innerText = "High School Program";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Camp Program";
            option.innerText = "Camp Program";
            select.append(option);

            var option = document.createElement('option');
            option.value = "College Counseling Program";
            option.innerText = "College Counseling Program";
            select.append(option);

            var option = document.createElement('option');
            option.value = "ESL Teacher Recruitment Program";
            option.innerText = "ESL Teacher Recruitment Program";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Likeshuo Program";
            option.innerText = "Likeshuo Program";
            select.append(option);

            var option = document.createElement('option');
            option.value = "Others";
            option.innerText = "Others";
            select.append(option);
        }
        else {
            var option = document.createElement('option');
            option.value = "Previous Staff Documentation";
            option.innerText = "Previous Staff Documentation";
            select.append(option);
        }
    }

    function onMiddleCategorySearchChange() {
        var category = $('#category_search').val();
        var mdCategory = $('#md_category_search').val();

        $('#sm_category_search').prop('disabled', false);
        var select = document.getElementById('sm_category_search');
        select.innerHTML = '<option value="">Select Sub-sub Category</option>';

        if (category === "" || mdCategory === "") {
            return;
        }


        if (category === "Official Common Templates") {
            if (mdCategory === "Program Template") {
                var option = document.createElement('option');
                option.value = "High School Program Template";
                option.innerText = "High School Program Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Camp Program Template";
                option.innerText = "Camp Program Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "College Couseling Template";
                option.innerText = "College Couseling Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "ESL Teacher Recruitment";
                option.innerText = "ESL Teacher Recruitment";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Likeshuo Program Template";
                option.innerText = "Likeshuo Program Template";
                select.append(option);
            }
            else if (mdCategory === "Contract Template") {
                var option = document.createElement('option');
                option.value = "High School Program Contract Template";
                option.innerText = "High School Program Contract Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Camp Program Contract Template";
                option.innerText = "Camp Program Contract Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "College Counseling Program Contract Template";
                option.innerText = "College Counseling Program Contract Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "ESL Teacher Recruitement Contract Template";
                option.innerText = "ESL Teacher Recruitement Contract Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Likeshuo Program Contract Template";
                option.innerText = "Likeshuo Program Contract Template";
                select.append(option);
            }
            else if (mdCategory === "Staff Report Template") {
                var option = document.createElement('option');
                option.value = "Office Weekly Meeting Report Template";
                option.innerText = "Office Weekly Meeting Report Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Businesss Trip Report";
                option.innerText = "Businesss Trip Report";
                select.append(option);
            }
            else {
                // Others
                $('#sm_category_search').prop('disabled', true);
                var select = document.getElementById('sm_category_search');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
        }
        else if (category === "HR & Administration Management") {
            if (mdCategory === "Hiring Template") {
                var option = document.createElement('option');
                option.value = "Job Offer Letter Template";
                option.innerText = "Job Offer Letter Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Employment Agreement Template";
                option.innerText = "Employment Agreement Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Performance Review Form Template";
                option.innerText = "Performance Review Form Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Employee Exit Memo Template";
                option.innerText = "Employee Exit Memo Template";
                select.append(option);
            }
            else if (mdCategory === "VI System") {
                var option = document.createElement('option');
                option.value = "Company Logo";
                option.innerText = "Company Logo";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Letter Head";
                option.innerText = "Letter Heade";
                select.append(option);

                var option = document.createElement('option');
                option.value = "PPT Template";
                option.innerText = "PPT Template";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Email Signature";
                option.innerText = "Email Signature";
                select.append(option);
            }
            else if (mdCategory === "Finance & Payroll") {
                var option = document.createElement('option');
                option.value = "Doposit Authorization";
                option.innerText = "Doposit Authorizationo";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Expense Report";
                option.innerText = "Expense Report";
                select.append(option);
            }
            else if (mdCategory === "Staff Documentation") {
                // Employee name_yyyy
                $('#sm_category_search').prop('disabled', true);
                var select = document.getElementById('sm_category_search');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
            else if (mdCategory === "Company Documentation") {
                var option = document.createElement('option');
                option.value = "Business License";
                option.innerText = "Business License";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Company Bank Information";
                option.innerText = "Company Bank Information";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Office Lease Agreement";
                option.innerText = "Office Lease Agreement";
                select.append(option);

                var option = document.createElement('option');
                option.value = "CSIET";
                option.innerText = "CSIET";
                select.append(option);

                var option = document.createElement('option');
                option.value = "BGE Manuel";
                option.innerText = "BGE Manuel";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Contract and Agreement";
                option.innerText = "Contract and Agreement";
                select.append(option);
            }
            else if (mdCategory === "Tax History") {
                // Tax History
                $('#sm_category_search').prop('disabled', true);
                var select = document.getElementById('sm_category_search');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
            else if (mdCategory === "Invoice History") {
                // Invoice History
                $('#sm_category_search').prop('disabled', true);
                var select = document.getElementById('sm_category_search');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
            else {
                // Others
                $('#sm_category_search').prop('disabled', true);
                var select = document.getElementById('sm_category_search');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
        }
        else if (category === "Promotional&Design Materials") {
            if (mdCategory === "Wording and PPT") {
                var option = document.createElement('option');
                option.value = "High School Program";
                option.innerText = "High School Program";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Camp";
                option.innerText = "Camp";
                select.append(option);

                var option = document.createElement('option');
                option.value = "College Couseling";
                option.innerText = "College Couseling";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Esl Teacher Recruitment";
                option.innerText = "Esl Teacher Recruitment";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Likeshuo";
                option.innerText = "Likeshuo";
                select.append(option);

                var option = document.createElement('option');
                option.value = "School Profile & Picture";
                option.innerText = "School Profile & Picture";
                select.append(option);
            }
            else if (mdCategory === "Pictures") {
                var option = document.createElement('option');
                option.value = "High School Program";
                option.innerText = "High School Program";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Camp";
                option.innerText = "Camp";
                select.append(option);

                var option = document.createElement('option');
                option.value = "College Couseling";
                option.innerText = "College Couseling";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Esl Teacher Recruitment";
                option.innerText = "Esl Teacher Recruitment";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Likeshuo";
                option.innerText = "Likeshuo";
                select.append(option);
            }
            else if (mdCategory === "Videos") {
                var option = document.createElement('option');
                option.value = "High School Program";
                option.innerText = "High School Program";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Camp";
                option.innerText = "Camp";
                select.append(option);

                var option = document.createElement('option');
                option.value = "College Couseling";
                option.innerText = "College Couseling";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Esl Teacher Recruitment";
                option.innerText = "Esl Teacher Recruitment";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Likeshuo";
                option.innerText = "Likeshuo";
                select.append(option);
            }
            else if (mdCategory === "BGE Partner High Schools") {
                var option = document.createElement('option');
                option.value = "Massachuessetts";
                option.innerText = "Massachuessetts";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Connecticut";
                option.innerText = "Connecticut";
                select.append(option);

                var option = document.createElement('option');
                option.value = "New Jersey";
                option.innerText = "New Jersey";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Pennsylvania";
                option.innerText = "Pennsylvania";
                select.append(option);

                var option = document.createElement('option');
                option.value = "California";
                option.innerText = "California";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Virginia";
                option.innerText = "Virginia";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Boarding Schools";
                option.innerText = "Boarding Schools";
                select.append(option);

                var option = document.createElement('option');
                option.value = "Colleges";
                option.innerText = "Colleges";
                select.append(option);
            }
            else {
                // Others
                $('#sm_category_search').prop('disabled', true);
                var select = document.getElementById('sm_category_search');
                select.innerHTML = '<option value="">Nothing..</option>';
            }
        }
        else if (category === "Program & Student Information") {
            $('#sm_category_search').prop('disabled', true);
            var select = document.getElementById('sm_category_search');
            select.innerHTML = '<option value="">Nothing..</option>';
        }
        else {
            $('#sm_category_search').prop('disabled', true);
            var select = document.getElementById('sm_category_search');
            select.innerHTML = '<option value="">Nothing..</option>';
        }
    }


    $('#category_upload').on('change', function () {
        onCategoryUploadChange();
    });

    $('#md_category_upload').on('change', function () {
        onMiddleCategoryUploadChange();
    });

    $('#category_search').on('change', function () {
        onCategorySearchChange();
    });

    $('#md_category_search').on('change', function () {
        onMiddleCategorySearchChange();
    });
});