from .utils import (
    JsonFile,
    RootPath,
    ColorPrint
)
from typing import List, Dict, Any, Set

SELECTED_OAS_FILE = "docs/selected-coingecko-pro-demo"


class EndpointSelector:
    def __init__(
        self,
        paths_to_select: List[str]
    ) -> None:
        self.paths_to_select = paths_to_select

    def run(self) -> None:
        target_oas = JsonFile.read_json(file_path="docs/coingecko")
        selected_oas = JsonFile.read_json(file_path="docs/default-oas")
        selected_oas["paths"] = self.select_endpoints(
            all_available_paths=target_oas.get("paths", {})
        )
        selected_oas["components"]["schemas"] = self.extract_relevant_schemas(
            oas=target_oas,
            selected_paths=selected_oas["paths"]
        )
        JsonFile.write_json(
            selected_oas,
            file_path=SELECTED_OAS_FILE
        )
        ColorPrint.print_success(f"Selected OAS saved to {RootPath.get_package_root() / SELECTED_OAS_FILE}.json")

    def select_endpoints(
        self,
        all_available_paths: Dict[str, Any]
    ) -> Dict[str, Any]:
        selected_paths_dict: Dict[str, Any] = {}
        found_onchain_count = 0
        not_found_paths: List[str] = []
        found_paths_count = 0
        for path_to_select in self.paths_to_select:
            if path_to_select in all_available_paths:
                selected_paths_dict[path_to_select] = all_available_paths[path_to_select]
                found_paths_count += 1
                if path_to_select.startswith("/onchain"):
                    found_onchain_count += 1
            else:
                not_found_paths.append(path_to_select)
        ColorPrint.print_info(
            f"Found and selected {found_paths_count} paths. "
        )
        if not_found_paths:
            ColorPrint.print_warning(
                f"The following {len(not_found_paths)} requested paths were not found in the target OAS: {', '.join(not_found_paths)}"
            )
        return selected_paths_dict

    def extract_schema_refs(
        self,
        obj: Any
    ) -> Set[str]:
        refs: Set[str] = set()
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key == "$ref" and isinstance(value, str) and value.startswith("#/components/schemas/"):
                    schema_name = value.split("/")[-1]
                    refs.add(schema_name)
                elif isinstance(value, (dict, list)):
                    refs.update(self.extract_schema_refs(value))
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    refs.update(self.extract_schema_refs(item))
        return refs

    def extract_relevant_schemas(
        self,
        oas: Dict[str, Any],
        selected_paths: Dict[str, Any]
    ) -> Dict[str, Any]:
        all_schemas = oas.get("components", {}).get("schemas", {})
        if not all_schemas:
            ColorPrint.print_info("No schemas found in the target OAS components.")
            return {}
        referenced_schema_names: Set[str] = set()
        for _, path_item in selected_paths.items():
            if isinstance(path_item, dict):
                for _, operation in path_item.items():
                    if isinstance(operation, dict):
                        referenced_schema_names.update(self.extract_schema_refs(operation))
        processed_schemas: Set[str] = set()
        schemas_to_process: List[str] = sorted(list(referenced_schema_names))
        final_selected_schemas: Dict[str, Any] = {}
        while schemas_to_process:
            schema_name = schemas_to_process.pop(0)
            if schema_name in processed_schemas:
                continue
            processed_schemas.add(schema_name)
            if schema_name in all_schemas:
                final_selected_schemas[schema_name] = all_schemas[schema_name]
                new_refs = self.extract_schema_refs(all_schemas[schema_name])
                for ref in new_refs:
                    if ref not in processed_schemas and ref not in schemas_to_process:
                        schemas_to_process.append(ref)
                schemas_to_process.sort()
        ColorPrint.print_info(f"Selected {len(final_selected_schemas)} schemas based on references in selected paths.")
        return dict(sorted(final_selected_schemas.items()))
