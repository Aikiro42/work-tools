function populateFormWithImages() {
  // Requires workspace permissions: Edit forms, access folders.
  
  // https://docs.google.com/forms/d/1MSoywBbJy1m4FCw6-okuE4xTj_yFhQgeGE--Ajn5Sa4/edit
  const formId = '1MSoywBbJy1m4FCw6-okuE4xTj_yFhQgeGE--Ajn5Sa4';
  // Original: https://drive.google.com/drive/folders/1aSP9LkP_V5bcMn4fR0gQLFxq_AAwqVc3
  // Compressed: https://drive.google.com/drive/folders/162vx6l8jRP0fTdwnAt-5LbP7P8ZDegqr
  const folderId = '162vx6l8jRP0fTdwnAt-5LbP7P8ZDegqr';
    
  const form = FormApp.openById(formId);
  const folder = DriveApp.getFolderById(folderId);
  const files = folder.getFiles();
  
  let imageFiles = [];
  
  // Collect all image files from the folder
  while (files.hasNext()) {
    let file = files.next();
    let fileName = file.getName().toLowerCase();
    if (fileName.endsWith('.png') || fileName.endsWith('.jpg') || fileName.endsWith('.jpeg')) {
      imageFiles.push(file);
    }
  }

  // Clear existing items if you want a fresh start (optional)
  let items = form.getItems();
  console.log("Resetting form...")
  for (let i = items.length - 1; i >= 0; i--) {
    form.deleteItem(i);
  }

  // Process images in groups of three
  for (let i = 0; i < imageFiles.length; i += 3) {
    let group = imageFiles.slice(i, i + 3);
    let sectionTitle = "Voting Section " + (Math.floor(i / 3) + 1);
    console.log(`Initializing ${sectionTitle}...`);
    
    // Add a Page Break (Section)
    form.addPageBreakItem().setTitle(sectionTitle);
    
    let imageNames = [];
    
    // Add the three images to the section
    group.forEach(file => {
      form.addImageItem()
          .setImage(file.getBlob())
          .setTitle(file.getName())
          .setAlignment(FormApp.Alignment.CENTER);
      imageNames.push(file.getName());
      console.log(`  Adding ${file.getName()}...`);
    });
    
    if (imageNames.length > 0) {
      // Add a checkbox question with the image names as options
      console.log(`  Adding checkboxes...`);
      form.addCheckboxItem()
          .setTitle("Select your favorite background(s) from this section:")
          .setChoiceValues(imageNames);
          
      // Add a remarks long anwer question
      console.log(`  Adding remarks...`);
      form.addParagraphTextItem()
          .setTitle("Remarks (Voting Section " + (Math.floor(i / 3) + 1) + ")")
    }
  }
  
  Logger.log('Form population complete.');
}