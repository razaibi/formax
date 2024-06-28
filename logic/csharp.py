def generate_csharp_class(json_data):
    elements = json_data["form"]["elements"]
    
    class_code = "using System.ComponentModel.DataAnnotations;\n\n"
    class_code += f"public class {json_data["backend"]["model"]}" + "{" + "\n\n"
    
    for element in elements:
        if "type" in element and "name" in element and "label" in element:
            element_type = element["type"]
            element_name = element["name"]
            element_label = element["label"]
            is_required = element.get("required", False)
            
            capitalized_name = element_name[0].upper() + element_name[1:]
            
            class_code += f"    [Display(Name = \"{element_label}\")]\n"
            if is_required:
                class_code += "    [Required]\n"
            class_code += f"    public string {capitalized_name} {{ get; set; }} // {element_type}\n\n"
    
    class_code += "}\n"
    
    return class_code