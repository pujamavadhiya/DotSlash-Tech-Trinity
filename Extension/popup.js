document.addEventListener('DOMContentLoaded', async function () {
    async function checkTermsAndConditions() {
    
      await new Promise(resolve => setTimeout(resolve, 5000));
  
     
      return "hello";
    }
  
    
    document.querySelector('.loader').style.display = 'block';
  
    try {
    
      const hasTermsAndConditions = await checkTermsAndConditions();
  
     
      document.querySelector('.loader').style.display = 'none';
  
      
      if (hasTermsAndConditions) {
        
        document.getElementById('points-container').innerHTML = '<h2>Terms and Conditions Found</h2>';
      } else {

        document.getElementById('points-container').innerHTML = '<h2>No Terms And Conditions Found</h2><div id="img-nodata"><img src="images/nodata.jpg"></div><ul id="points-list"></ul>';
      }
    } catch (error) {
      console.error('Error during checkTermsAndConditions:', error);

    }
  });
  