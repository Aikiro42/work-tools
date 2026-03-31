function updateFormWithoutBloat() {
  const formId = '1MSoywBbJy1m4FCw6-okuE4xTj_yFhQgeGE--Ajn5Sa4';
  const folderId = '162vx6l8jRP0fTdwnAt-5LbP7P8ZDegqr'; // Use your RESIZED folder ID here
  
  const form = FormApp.openById(formId);
  const folder = DriveApp.getFolderById(folderId);
  
  // 1. GET & SORT FILES
  const files = folder.getFiles();
  let imageFiles = [];
  while (files.hasNext()) {
    let file = files.next();
    let name = file.getName().toLowerCase();
    if (name.endsWith('.png') || name.endsWith('.jpg') || name.endsWith('.jpeg')) {
      imageFiles.push(file);
    }
  }
  // Sort naturally (1, 2, 10...)
  imageFiles.sort((a, b) => a.getName().localeCompare(b.getName(), undefined, {numeric: true, sensitivity: 'base'}));

  // 2. GET EXISTING ITEMS
  // We will modify this array "live" as we go
  let items = form.getItems();
  let cursor = 0; // Tracks our current position in the form

  // --- HELPER: ENSURE ITEM TYPE ---
  // Checks if item at 'cursor' matches desired type. 
  // If yes: returns it. 
  // If no: deletes current, adds new, moves to cursor, returns new.
  function ensureItem(type, title) {
    let item = items[cursor];
    
    // Check if item exists and matches type
    if (item && item.getType() === type) {
      // MATCH! Just update the title.
      if (title) item.setTitle(title);
      // console.log(`[Reusing] ID ${item.getId()} at index ${cursor}`);
      return item;
    } 
    
    // MISMATCH! (Or end of form). Delete current if it exists but is wrong type.
    if (item) {
      form.deleteItem(cursor); 
    }
    
    // Create new (adds to bottom)
    let newItem;
    if (type === FormApp.ItemType.PAGE_BREAK) newItem = form.addPageBreakItem();
    else if (type === FormApp.ItemType.IMAGE) newItem = form.addImageItem();
    else if (type === FormApp.ItemType.CHECKBOX) newItem = form.addCheckboxItem();
    else if (type === FormApp.ItemType.PARAGRAPH_TEXT) newItem = form.addParagraphTextItem();
    
    if (title) newItem.setTitle(title);
    
    // Move from bottom to current cursor position
    form.moveItem(newItem, cursor);
    
    // Refresh items array because indices shifted
    items = form.getItems();
    
    console.log(`[Created New] at index ${cursor}`);
    return newItem;
  }

  // 3. THE LOOP
  for (let i = 0; i < imageFiles.length; i += 3) {
    let group = imageFiles.slice(i, i + 3);
    let sectionTitle = "Voting Section " + (Math.floor(i / 3) + 1);
    
    console.log(`Updating ${sectionTitle}...`);
    
    // A. SECTION HEADER (Page Break)
    ensureItem(FormApp.ItemType.PAGE_BREAK, sectionTitle);
    cursor++;

    let imageNames = [];

    // B. IMAGES
    group.forEach(file => {
      // Ensure we have an Image Item here
      let imgItem = ensureItem(FormApp.ItemType.IMAGE, file.getName());
      
      // *** THE MAGIC: SWAP BLOB IN PLACE ***
      // We overwrite the image data without changing the Item ID
      imgItem.asImageItem()
             .setImage(file.getBlob())
             .setAlignment(FormApp.Alignment.CENTER);
      
      imageNames.push(file.getName());
      cursor++;
    });

    // C. QUESTIONS
    if (imageNames.length > 0) {
      // Checkbox
      let cbItem = ensureItem(FormApp.ItemType.CHECKBOX, "Select your favorite background(s) from this section:");
      cbItem.asCheckboxItem().setChoiceValues(imageNames);
      cursor++;

      // Remarks
      ensureItem(FormApp.ItemType.PARAGRAPH_TEXT, "Remarks (" + sectionTitle + ")");
      cursor++;
    }
  }

  // 4. CLEANUP LEFTOVERS
  // If the new script has FEWER items than the old form, delete the tail.
  items = form.getItems(); // Refresh one last time
  while (items.length > cursor) {
    console.log(`Deleting extra item at index ${cursor}...`);
    form.deleteItem(cursor);
    items = form.getItems(); // Refresh needed after delete
  }

  Logger.log('Form update complete. IDs preserved where possible.');
}