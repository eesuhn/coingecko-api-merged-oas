from .utils import (
    load_json,
    save_json,
    print_success,
    get_package_root,
    print_info
)


class EndpointSelector:
    def __init__(
        self,
        non_onchain_count: int = 10,
        onchain_count: int = 5
    ) -> None:
        self.non_onchain_count = non_onchain_count
        self.onchain_count = onchain_count

    def run(self) -> None:
        target_oas = load_json(filename="docs/coingecko")
        selected_oas = load_json(filename="docs/default-oas")
        selected_oas["paths"] = self.select_endpoints(
            paths=target_oas["paths"]
        )
        selected_oas["components"]["schemas"] = self.extract_relevant_schemas(
            oas=target_oas,
            selected_paths=selected_oas["paths"]
        )
        save_json(
            selected_oas,
            filename="docs/selected-coingecko"
        )
        print_success(f"Selected OAS at {get_package_root() / 'docs/selected-coingecko.json'}")

    def select_endpoints(
        self,
        paths: dict
    ) -> dict:
        onchain_paths = {}
        non_onchain_paths = {}
        for path, details in paths.items():
            if path.startswith("/onchain"):
                onchain_paths[path] = details
            else:
                non_onchain_paths[path] = details
        selected_onchain = dict(
            list(onchain_paths.items())[:self.onchain_count]
        )
        selected_non_onchain = dict(
            list(non_onchain_paths.items())[:self.non_onchain_count]
        )
        selected_paths = {**selected_non_onchain, **selected_onchain}
        print_info(f"Selected {len(selected_paths)} paths: {len(selected_onchain)} from /onchain")
        return selected_paths

    def extract_schema_refs(
        self,
        obj: dict
    ) -> set:
        refs = set()
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
        oas: dict,
        selected_paths: dict
    ) -> dict:
        all_schemas = oas["components"]["schemas"]
        referenced_schema_names = set()
        for _, path_item in selected_paths.items():
            for _, operation in path_item.items():
                if isinstance(operation, dict):
                    referenced_schema_names.update(self.extract_schema_refs(operation))
        processed_schemas = set()
        schemas_to_process = sorted(list(referenced_schema_names))
        while schemas_to_process:
            schema_name = schemas_to_process.pop(0)
            if schema_name in processed_schemas:
                continue
            processed_schemas.add(schema_name)
            if schema_name in all_schemas:
                new_refs = self.extract_schema_refs(all_schemas[schema_name])
                new_refs_to_add = [
                    ref for ref in new_refs if ref not in processed_schemas and ref not in schemas_to_process
                ]
                schemas_to_process.extend(sorted(new_refs_to_add))
        selected_schemas = {}
        for name in sorted(processed_schemas):
            if name in all_schemas:
                selected_schemas[name] = all_schemas[name]
        print_info(f"Selected {len(selected_schemas)} schemas")
        return selected_schemas
