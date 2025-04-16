using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Newtonsoft.Json;

namespace ClaudeMCP_RevitAddin
{
    [Transaction(TransactionMode.Manual)]
    public class ClaudeMCPCommand : IExternalCommand
    {
        private const string MCP_SERVER_URL = "http://localhost:8000";
        private readonly HttpClient _httpClient = new HttpClient();

        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            try
            {
                UIApplication uiApp = commandData.Application;
                UIDocument uiDoc = uiApp.ActiveUIDocument;
                Document doc = uiDoc.Document;

                // Show input dialog for design requirements
                var inputForm = new DesignInputForm();
                if (inputForm.ShowDialog() != System.Windows.Forms.DialogResult.OK)
                {
                    return Result.Cancelled;
                }

                // Prepare design request
                var designRequest = new
                {
                    action = "generate_design",
                    requirements = new
                    {
                        area = inputForm.TotalArea,
                        bedrooms = inputForm.Bedrooms,
                        bathrooms = inputForm.Bathrooms,
                        style = inputForm.Style,
                        additional_requirements = inputForm.AdditionalRequirements
                    }
                };

                string jsonData = JsonConvert.SerializeObject(designRequest);
                var content = new StringContent(jsonData, Encoding.UTF8, "application/json");

                // Show progress dialog
                using (var progressDialog = new ProgressDialog("Generating Design..."))
                {
                    progressDialog.Show();

                    // Send request to MCP server
                    var response = _httpClient.PostAsync($"{MCP_SERVER_URL}/generate", content).Result;
                    if (response.IsSuccessStatusCode)
                    {
                        string responseContent = response.Content.ReadAsStringAsync().Result;
                        var result = JsonConvert.DeserializeObject<dynamic>(responseContent);

                        // Create the design in Revit
                        using (Transaction tx = new Transaction(doc, "Create Design"))
                        {
                            tx.Start();
                            CreateDesign(doc, result.design);
                            tx.Commit();
                        }

                        TaskDialog.Show("Success", "Design has been created successfully!");
                        return Result.Succeeded;
                    }
                    else
                    {
                        TaskDialog.Show("Error", $"Failed to generate design: {response.StatusCode}");
                        return Result.Failed;
                    }
                }
            }
            catch (Exception ex)
            {
                message = ex.Message;
                return Result.Failed;
            }
        }

        private void CreateDesign(Document doc, dynamic design)
        {
            // Create levels
            double baseLevel = 0;
            foreach (var level in design.levels)
            {
                Level.Create(doc, (double)level.elevation);
            }

            // Create walls
            foreach (var wall in design.walls)
            {
                Line wallLine = Line.CreateBound(
                    new XYZ((double)wall.start.x, (double)wall.start.y, baseLevel),
                    new XYZ((double)wall.end.x, (double)wall.end.y, baseLevel)
                );
                Wall.Create(doc, wallLine, (ElementId)wall.type_id, (ElementId)wall.level_id, 3.0, 0, false, false);
            }

            // Create rooms
            foreach (var room in design.rooms)
            {
                // Create room boundary
                var boundary = new List<Curve>();
                foreach (var point in room.boundary)
                {
                    boundary.Add(Line.CreateBound(
                        new XYZ((double)point.x, (double)point.y, baseLevel),
                        new XYZ((double)point.next.x, (double)point.next.y, baseLevel)
                    ));
                }

                // Create room
                doc.Create.NewRoomBoundaryLines(
                    doc.ActiveView.SketchPlane,
                    boundary,
                    doc.ActiveView
                );
            }

            // Create doors and windows
            foreach (var opening in design.openings)
            {
                FamilySymbol symbol = doc.GetElement(new ElementId((int)opening.type_id)) as FamilySymbol;
                if (symbol != null && !symbol.IsActive)
                {
                    symbol.Activate();
                }

                doc.Create.NewFamilyInstance(
                    new XYZ((double)opening.location.x, (double)opening.location.y, baseLevel),
                    symbol,
                    doc.GetElement(new ElementId((int)opening.host_id)) as Wall,
                    StructuralType.NonStructural
                );
            }
        }
    }

    public class DesignInputForm : System.Windows.Forms.Form
    {
        private System.Windows.Forms.TextBox txtArea;
        private System.Windows.Forms.TextBox txtBedrooms;
        private System.Windows.Forms.TextBox txtBathrooms;
        private System.Windows.Forms.ComboBox cmbStyle;
        private System.Windows.Forms.TextBox txtAdditional;
        private System.Windows.Forms.Button btnOK;
        private System.Windows.Forms.Button btnCancel;

        public double TotalArea => double.Parse(txtArea.Text);
        public int Bedrooms => int.Parse(txtBedrooms.Text);
        public int Bathrooms => int.Parse(txtBathrooms.Text);
        public string Style => cmbStyle.SelectedItem.ToString();
        public string AdditionalRequirements => txtAdditional.Text;

        public DesignInputForm()
        {
            InitializeComponent();
        }

        private void InitializeComponent()
        {
            this.txtArea = new System.Windows.Forms.TextBox();
            this.txtBedrooms = new System.Windows.Forms.TextBox();
            this.txtBathrooms = new System.Windows.Forms.TextBox();
            this.cmbStyle = new System.Windows.Forms.ComboBox();
            this.txtAdditional = new System.Windows.Forms.TextBox();
            this.btnOK = new System.Windows.Forms.Button();
            this.btnCancel = new System.Windows.Forms.Button();

            // Area
            this.txtArea.Location = new System.Drawing.Point(120, 20);
            this.txtArea.Size = new System.Drawing.Size(150, 20);
            System.Windows.Forms.Label lblArea = new System.Windows.Forms.Label();
            lblArea.Text = "Total Area (m²):";
            lblArea.Location = new System.Drawing.Point(20, 23);

            // Bedrooms
            this.txtBedrooms.Location = new System.Drawing.Point(120, 50);
            this.txtBedrooms.Size = new System.Drawing.Size(150, 20);
            System.Windows.Forms.Label lblBedrooms = new System.Windows.Forms.Label();
            lblBedrooms.Text = "Number of Bedrooms:";
            lblBedrooms.Location = new System.Drawing.Point(20, 53);

            // Bathrooms
            this.txtBathrooms.Location = new System.Drawing.Point(120, 80);
            this.txtBathrooms.Size = new System.Drawing.Size(150, 20);
            System.Windows.Forms.Label lblBathrooms = new System.Windows.Forms.Label();
            lblBathrooms.Text = "Number of Bathrooms:";
            lblBathrooms.Location = new System.Drawing.Point(20, 83);

            // Style
            this.cmbStyle.Location = new System.Drawing.Point(120, 110);
            this.cmbStyle.Size = new System.Drawing.Size(150, 20);
            this.cmbStyle.Items.AddRange(new string[] { "Modern", "Traditional", "Minimalist", "Contemporary" });
            this.cmbStyle.SelectedIndex = 0;
            System.Windows.Forms.Label lblStyle = new System.Windows.Forms.Label();
            lblStyle.Text = "Architectural Style:";
            lblStyle.Location = new System.Drawing.Point(20, 113);

            // Additional Requirements
            this.txtAdditional.Location = new System.Drawing.Point(120, 140);
            this.txtAdditional.Size = new System.Drawing.Size(150, 60);
            this.txtAdditional.Multiline = true;
            System.Windows.Forms.Label lblAdditional = new System.Windows.Forms.Label();
            lblAdditional.Text = "Additional Requirements:";
            lblAdditional.Location = new System.Drawing.Point(20, 143);

            // Buttons
            this.btnOK.Text = "OK";
            this.btnOK.DialogResult = System.Windows.Forms.DialogResult.OK;
            this.btnOK.Location = new System.Drawing.Point(120, 220);
            this.btnCancel.Text = "Cancel";
            this.btnCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.btnCancel.Location = new System.Drawing.Point(200, 220);

            // Form
            this.Text = "Design Requirements";
            this.ClientSize = new System.Drawing.Size(300, 260);
            this.Controls.AddRange(new System.Windows.Forms.Control[] {
                lblArea, txtArea,
                lblBedrooms, txtBedrooms,
                lblBathrooms, txtBathrooms,
                lblStyle, cmbStyle,
                lblAdditional, txtAdditional,
                btnOK, btnCancel
            });
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.MinimizeBox = false;
            this.MaximizeBox = false;
        }
    }

    public class ProgressDialog : IDisposable
    {
        private readonly TaskDialog _dialog;

        public ProgressDialog(string message)
        {
            _dialog = new TaskDialog("Claude MCP")
            {
                MainInstruction = message,
                MainContent = "Please wait while we generate your design...",
                CommonButtons = TaskDialogCommonButtons.None
            };
        }

        public void Show()
        {
            _dialog.Show();
        }

        public void Dispose()
        {
            // Cleanup if needed
        }
    }
} 