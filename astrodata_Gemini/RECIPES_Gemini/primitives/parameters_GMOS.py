{       'addBPM': {'postpend':
                          {
                           'default': '_bpm' , #value to be post pended to this primitives outputs
                          'recipeOverride': True,
                          'type': 'str',
                          'userOverride':False    
                           }
                          },

        'biasCorrect':{'fl_over':
                        {
                          'default': False , 
                          'recipeOverride': True,
                          'type': 'bool',
                          'userOverride':True                                      
                         },
                         'fl_trim':
                         {
                          'default': False , 
                          'recipeOverride': False,
                          'type': 'bool',
                          'userOverride':False    
                          },
                          'fl_vardq':
                          {
                           'default': True ,
                          'recipeOverride': True,
                          'type': 'bool',
                          'userOverride':True    
                           },
                          'postpend':
                          {
                           'default': '_biassub' , #value to be post pended to this primitives outputs
                          'recipeOverride': True,
                          'type': 'str',
                          'userOverride':False    
                           }
                          },
        'flatCorrect':{
                       'postpend':
                       {
                        'default': '_flatcorrected' , 
                          'recipeOverride': True,
                          'type': 'str',
                          'userOverride':False  
                        }
                       },
        'mosaicDetectors':{
                  'fl_paste':
                          {
                           'default': False ,
                          'recipeOverride': True,
                          'type': 'bool',
                          'userOverride':True,  
                          'tag':['cl_iraf','ui_advanced'], #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                           },
                  'postpend':
                       {
                        'default': '_mosaic' , 
                          'recipeOverride': True,
                          'type': 'str',
                          'userOverride':False  ,
                        'tag':['cl_iraf','ui_advanced'], #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                        },
                    'interp_function':  #this is the geointer parameters new name for easier reading to the user
                          {
                           'default': 'linear' ,
                          'recipeOverride': True,
                          'type': 'str',
                          'userOverride':True,  
                          'tag':['cl_iraf','ui_advanced'], #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                           },
                           
                  },
    'normalizeFlat':{
                        'fl_over':
                        {
                          'default': False , 
                          'recipeOverride': False,
                          'type': 'bool',
                          'userOverride':False,
                          'tag':['cl_iraf','ui_advanced'], #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                         },
                         'fl_trim':
                         {
                          'default': False , 
                          'recipeOverride': False,
                          'type': 'bool',
                          'userOverride':False,    
                          'tag':['cl_iraf','ui_advanced'], #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                         
                          },
                          'fl_vardq':
                          {
                           'default': True ,
                          'recipeOverride': True,
                          'type': 'bool',
                          'userOverride':True,  
                          'tag':['cl_iraf','ui_advanced'], #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                           },
                          'postpend':
                          {
                           'default': '_normalized' , #value to be post pended to this primitives outputs (used by CLManager not CL directly for this prim)
                          'recipeOverride': True,
                          'type': 'str',
                          'userOverride':False    
                           },
                          'fl_bias':
                          {
                           'default': False , 
                          'recipeOverride': False,
                          'type': 'bool',
                          'userOverride':False, 
                          'tag':['cl_iraf','ui_advanced'], #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
                           }
                          },
                                                   
        'overscanSubtract':{'fl_trim':
                         {
                          'default': False , 
                          'recipeOverride': False,
                          'type': 'bool',
                          'userOverride':False    
                          },
                          'fl_vardq':
                          {
                           'default': False ,
                          'recipeOverride': True,
                          'type': 'bool',
                          'userOverride':True    
                           },
                          'postpend':
                          {
                           'default': '_oversubed' , #value to be post pended to this primitives outputs
                          'recipeOverride': True,
                          'type': 'str',
                          'userOverride':False    
                           },
                           'biassec':
                           {
                            'default': '[1:25,1:2304],[1:32,1:2304],[1025:1056,1:2304]' ,
                            'recipeOverride': True,
                            'type': 'str',
                            'userOverride':True
                            }
                        },
        'overscanTrim':{'postpend':
                          {
                           'default': '_overtrimd' , #value to be post pended to this primitives outputs
                          'recipeOverride': True,
                          'type': 'str',
                          'userOverride':False    
                           }
                        },
        'storeProcessedBias':{'clob':
                              {
                                'default': False,
                                'recipeOverride': True,
                                'type': 'bool',
                                'userOverride':True  
                               }
                              } ,
        'storeProcessedFlat':{'clob':
                              {
                                'default': False,
                                'recipeOverride': True,
                                'type': 'bool',
                                'userOverride':True  
                               }
                              } ,
        
}
