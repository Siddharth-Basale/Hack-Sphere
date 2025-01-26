document.getElementById("invoice-form").addEventListener("submit", (e) => {
    e.preventDefault();

    const company = document.getElementById("company").value;
    const invoice = document.getElementById("invoice").value;

    fetch("/update_invoice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company, invoice }),
    }).then(() => {
        alert("Invoice added successfully!");
        document.getElementById("invoice-form").reset();
    });
});

document.getElementById("load-data-btn").addEventListener("click", () => {
    fetch("/get_invoices")
        .then((response) => response.json())
        .then((data) => {
            const tableBody = document.getElementById("invoice-table-body");
            tableBody.innerHTML = "";

            if (data.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="4">No data available</td></tr>`;
                return;
            }

            data.forEach(([company, invoice, status]) => {
                const row = document.createElement("tr");

                const companyCell = document.createElement("td");
                companyCell.textContent = company;

                const invoiceCell = document.createElement("td");
                invoiceCell.textContent = invoice;
                if (status === "Invalid") invoiceCell.contentEditable = true;

                const statusCell = document.createElement("td");
                statusCell.textContent = status;

                const actionCell = document.createElement("td");
                if (status === "Invalid") {
                    const makeValidBtn = document.createElement("button");
                    makeValidBtn.textContent = "Make Valid";
                    makeValidBtn.addEventListener("click", () => {
                        fetch("/edit_invoice", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({
                                original_invoice: invoice,
                                updated_invoice: invoiceCell.textContent.trim(),
                            }),
                        }).then(() => {
                            statusCell.textContent = "Valid";
                            alert("Invoice marked as valid!");
                        });
                    });
                    actionCell.appendChild(makeValidBtn);
                } else {
                    const finalizeBtn = document.createElement("button");
                    finalizeBtn.textContent = "Okay";
                    finalizeBtn.addEventListener("click", () => {
                        fetch("/finalize_invoice", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ invoice }),
                        }).then(() => {
                            row.remove();
                            alert("Invoice finalized!");
                        });
                    });
                    actionCell.appendChild(finalizeBtn);
                }

                row.appendChild(companyCell);
                row.appendChild(invoiceCell);
                row.appendChild(statusCell);
                row.appendChild(actionCell);

                tableBody.appendChild(row);
            });
        });
});
